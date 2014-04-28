from django.contrib import admin
from chirp.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Chirp)
admin.site.register(TaggedChirps)
admin.site.register(Hashtag)