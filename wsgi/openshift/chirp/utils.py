from chirp.models import *
from chirp.forms import *
from itertools import chain
from django.contrib.auth.models import User
import operator

def getAllChirps(user):
    userProfile = UserProfile.objects.get(user=user)
    chirps = Chirp.objects.filter(userProfile = userProfile)
    chirps = set(chain(chirps, TaggedChirps.objects.get(userProfile=userProfile).taggedIn.all()))
    for f in userProfile.follows.all():
        profile = UserProfile.objects.get(user=f.user)
        chirps = set(chain(chirps, Chirp.objects.filter(userProfile=profile, isPrivate=False)))
    chirps = sorted(chirps, key=lambda t: t.timestamp, reverse=True)

    return chirps;

def getPublicUserChirps(username):
    user = User.objects.get(username=username)
    userProfile = UserProfile.objects.get(user=user)
    chirps = Chirp.objects.filter(userProfile = userProfile)
    chirps = set(chain(chirps, TaggedChirps.objects.get(userProfile=userProfile).taggedIn.all()))
    chirps = sorted(chirps, key=lambda t: t.timestamp, reverse=True)
    
    return chirps;
    
# is user1 following user2
def isFollowing(user1, user2):
    user1Profile = UserProfile.objects.get(user=user1)
    user2Profile = UserProfile.objects.get(user=user2)
    
    return user1Profile.follows.filter(pk=user2Profile.id).exists()

def getUserData(user):
    profile = UserProfile.objects.get(user=user)
    userData = {'numChirps': Chirp.objects.filter(userProfile = profile).count(), 'numFollowing': profile.follows.all().count(), 'numFollowers': profile.numFollowers}
    
    return userData;