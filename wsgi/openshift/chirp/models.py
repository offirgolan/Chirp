from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default_profile.png')
    numFollowers = models.IntegerField(default=0, blank=True)
    
    def __unicode__(self):
        return self.user.username
            
class Chirp(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    message = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=True)
    isPrivate = models.BooleanField()
        
    def __unicode__(self):
        return self.message
    
    class Meta:
        ordering = ('timestamp',)
       
class TaggedChirps(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    taggedIn = models.ManyToManyField(Chirp, symmetrical=False, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=True)
    
    def __unicode__(self):
        return self.userProfile.user.username

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=140)
    chirps = models.ManyToManyField(Chirp, symmetrical=False, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=True)
                
    def __unicode__(self):
        return self.hashtag