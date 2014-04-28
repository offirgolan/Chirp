from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'chirp.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', 'chirp.views.user_signup'),
    url(r'^login/', 'chirp.views.user_login'),
    url(r'^logout/', 'chirp.views.user_logout'),
    url(r'^updateProfile/', 'chirp.views.user_profile_update'),
    url(r'^autoCompleteSearch/', 'chirp.views.autocomplete_search'),
    url(r'^search/', 'chirp.views.search'),
    url(r'^(?P<username>\w+)/updateChirps', 'chirp.views.update_chirps'),
    url(r'^(?P<username>\w+)/updateUserData', 'chirp.views.update_user_data'),
    url(r'^dashboard/', 'chirp.views.dashboard'),
    url(r'^compose/', 'chirp.views.compose_chirp'),
    url(r'^tag/(?P<hashtag>\w+)', 'chirp.views.view_hashtag'),
    url(r'^(?P<username>\w+)/follow', 'chirp.views.follow_user'),
    url(r'^(?P<username>\w+)/unfollow', 'chirp.views.unfollow_user'),
    url(r'^(?P<username>\w+)/$', 'chirp.views.user'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )
