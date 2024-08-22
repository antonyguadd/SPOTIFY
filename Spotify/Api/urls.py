from django.urls import path
from .views import AuthenticationURL, CheckAuthentication, CurrentSong, spotify_redirect
from .views import CreateUserView


urlpatterns = [
    path("authorize", AuthenticationURL.as_view(), name="authorize"),
    path("redirect", spotify_redirect, name="spotify-redirect"),
    path("check-auth", CheckAuthentication.as_view(), name="check-auth"),
    path("current-song", CurrentSong.as_view(), name="current-song"),
    
]
