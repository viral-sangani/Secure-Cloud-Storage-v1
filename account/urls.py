from django.urls import path, include
from account.api import RegisterAPI

# /api/auth/*
urlpatterns = [
    path('', include('rest_auth.urls')),
    path('register/', RegisterAPI.as_view()),
]
