from django.urls import path, include
from account.api import RegisterAPI, UserAPI

# /api/auth/*
urlpatterns = [
    path('', include('rest_auth.urls')),
    path('register/', RegisterAPI.as_view()),
    path('user/',UserAPI.as_view())
]
