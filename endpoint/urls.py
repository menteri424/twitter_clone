from tweet.models import Tweet
from django.urls import path
import endpoint.views as views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("tweet/", views.TweetView.as_view(), name="tweet"),
]
