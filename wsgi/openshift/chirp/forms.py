# Import the forms library to create forms
from django import forms
from chirp.models import *
from django.contrib.auth.hashers import check_password


# Create form class for the Registration form
class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'})) 
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()
            
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Email already exists.')
        return email

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'})) 
    
    class Meta:
        model = User
        fields = ('username', 'password')

class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        
class ComposeChirpForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Compose new Chirp...', 'maxlength': 140}))

                 