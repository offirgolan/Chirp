#from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.shortcuts import render, render_to_response
from chirp.models import *
from chirp.forms import *
from chirp.utils import *
from chirp.twittilize import *
from django.http import HttpResponse, HttpResponseRedirect
from itertools import chain
import json
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    signupForm = UserRegistrationForm()
    loginForm = UserLoginForm()

    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    return render(request, "home/index.html", { "signup_form" : signupForm, "login_form" : loginForm })

@login_required
def dashboard(request):
    compose_chirp_form = ComposeChirpForm()
    chirps = getAllChirps(request.user)
    profile = UserProfile.objects.get(user=request.user)
    profile_pic = profile.profile_pic
    
    #Update Profile Form
    update_profile_form = UpdateProfileForm(initial={
        'first_name': request.user.first_name, 'last_name': request.user.last_name, 
        'email': request.user.email
    })
        
    return render_to_response('user/index.html', {'showFollow': False, 'compose': True, 'chirps': chirps, 'user': request.user, 'compose_chirp_form' : compose_chirp_form, 'currUser': request.user, 'profile_pic': profile_pic, 'update_profile_form': update_profile_form, 'userData': getUserData(request.user)}, RequestContext(request))

@login_required
def user(request, username):
    user = User.objects.get(username=username)
    compose_chirp_form = ComposeChirpForm()
    
    compose = False
    if(username == request.user.username):
        compose = True
        showFollow = False
        following = True
    else:
        following = isFollowing(request.user,user)
        showFollow = True
        
    #Update Profile Form
    update_profile_form = UpdateProfileForm(initial={
        'first_name': request.user.first_name, 'last_name': request.user.last_name, 
        'email': request.user.email
    })
    
    chirps = getPublicUserChirps(username)
    profile_pic = UserProfile.objects.get(user=user).profile_pic
    return render_to_response('user/index.html', {'showFollow': showFollow, 'isFollowing': following, 'compose': compose, 'chirps': chirps, 'user': request.user, 'compose_chirp_form' : compose_chirp_form, 'currUser': user, 'profile_pic': profile_pic, 'update_profile_form': update_profile_form, 'userData': getUserData(user)}, RequestContext(request))

def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
    
        if form.is_valid():
            user = form.save()
            userProfile = UserProfile(user=user)
            userProfile.save()
            
            taggedProfile = TaggedChirps(userProfile=userProfile)
            taggedProfile.save()
            
            user.set_password(user.password)
            user.save()
            
            # Authenticate and login user
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            
            # Redirect user to their profile
            response = {} 
            response['redirect'] = '/dashboard'           
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        form = UserRegistrationForm()
            
    return render(request, "home/signup.html", { "signup_form" : form })
    
def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response = {} 
                response['redirect'] = '/dashboard'           
                return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            form.errors['__all__'] = form.error_class(["Username or password not found."])
    else:
        form = LoginForm()
        
    return render(request, "home/login.html", { "login_form" : form })

@login_required   
def user_profile_update(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)        
        userEmailCount = User.objects.filter(email=form.data['email']).count()
        if userEmailCount > 0 and form.data['email'] != request.user.email:
            form.errors['__all__'] = form.error_class(["Email already exists."])
        else:
            user = form.save()
            if len(request.POST['profile_pic']) > 0:
                profilePic = request.FILES['profile_pic']
                userProfile = UserProfile.objects.get(user=request.user)
                userProfile.profile_pic = profilePic
                userProfile.save()
            user.save()
    
    #Update Profile Form
    form = UpdateProfileForm(initial={
        'first_name': request.user.first_name, 'last_name': request.user.last_name, 
        'email': request.user.email
    })
    
    profile_pic = UserProfile.objects.get(user=request.user).profile_pic
            
    return render_to_response("user/updateProfile.html", { "update_profile_form" : form, 'profile_pic': profile_pic }, RequestContext(request))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def compose_chirp(request):
    form = ComposeChirpForm()
    if request.method == 'POST':
        message = twittilize(request.POST['message'], autoescape=True)
        chirp = Chirp(userProfile=UserProfile.objects.get(user=request.user), message=message, isPrivate=False);
        chirp.save()
        
        # Save the chirp to its proper hashtag
        hashtags = re.findall(hashtags_re, request.POST['message'])
        for hashtag in hashtags:
            tagName = hashtag.replace("#", "")
            hashCount = Hashtag.objects.filter(hashtag=tagName).count()
            if hashCount == 0:
                newTag = Hashtag(hashtag=tagName)
                newTag.save()
                newTag.chirps.add(chirp)
                newTag.save()
            else:
                tag = Hashtag.objects.get(hashtag=tagName)
                tag.chirps.add(chirp)
                tag.save()
        
        usernames = re.findall(usernames_re, request.POST['message'])
        for u in usernames:
            username = u.replace("@", "")
            if request.user.username == username:
                continue
            user = User.objects.get(username=username)
            taggedProfile = TaggedChirps.objects.get(userProfile= UserProfile.objects.get(user=user))
            taggedProfile.taggedIn.add(chirp)
            taggedProfile.save()
    
    return render_to_response('user/compose.html', {'compose_chirp_form':form}, RequestContext(request))

@login_required
def follow_user(request, username):
    followProfile = UserProfile.objects.get(user=User.objects.get(username=username))
    followProfile.numFollowers += 1
    followProfile.save()
    profile = UserProfile.objects.get(user=request.user)  
    profile.follows.add(followProfile)
    profile.save()    
    return HttpResponseRedirect('/' + username)

@login_required
def unfollow_user(request, username):
    followProfile = UserProfile.objects.get(user=User.objects.get(username=username))
    followProfile.numFollowers -= 1
    followProfile.save()
    profile = UserProfile.objects.get(user=request.user)  
    profile.follows.remove(followProfile)
    profile.save()    
    return HttpResponseRedirect('/' + username)
 
@login_required   
def update_chirps(request, username):     
    if(username == 'dashboard'):
        chirps = getAllChirps(request.user)
    else:
        chirps = getPublicUserChirps(username)

    return render(request, "user/chirps.html", { "chirps" : chirps })
    
@login_required   
def update_user_data(request, username):     
    if(username == 'dashboard'):
        data = getUserData(request.user)
    else:
        data = getUserData(User.objects.get(username=username))

    return render(request, "user/userData.html", { "userData" : data })
    
@login_required   
def view_hashtag(request, hashtag):     
    tag = Hashtag.objects.get(hashtag=hashtag)
    chirps = sorted(tag.chirps.all(), key=lambda t: t.timestamp, reverse=True)
    
    return render_to_response('user/hashtag.html', {'hashtag': hashtag, 'chirps': chirps, 'user': request.user}, RequestContext(request))

@login_required   
def search(request):   
    q = request.GET['query']
    response = {} 
    
    if "#" in q:
        query = q.replace("#", "")
        if Hashtag.objects.filter(hashtag=query).count() != 0:
            response['redirect'] = '/tag/' + query
    elif "@" in q:
        query = q.replace("@", "")
        if User.objects.filter(username=query).count() != 0:
            response['redirect'] = '/' + query
    
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required   
def autocomplete_search(request):     
    if request.is_ajax():
            q = request.GET.get('term', '')
            if "#" in q:
                # %23 is the symbol for # in uri
                query = q.replace("#", "")
                hashtags = Hashtag.objects.filter(hashtag__icontains = query )[:20]
                results = []
                for tag in hashtags:
                    tag_json = {}
                    tag_json['id'] = tag.id
                    tag_json['label'] = '#' + tag.hashtag
                    tag_json['value'] = '#' + tag.hashtag
                    results.append(tag_json)
                data = json.dumps(results)
            elif "@" in q:
                query = q.replace("@", "")
                users = User.objects.filter(username__icontains = query )[:20]
                results = []
                for user in users:
                    user_json = {}
                    user_json['id'] = user.id
                    user_json['label'] = '@' + user.username
                    user_json['value'] = '@' + user.username
                    results.append(user_json)
                data = json.dumps(results)
            else:
                results = []
                data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)