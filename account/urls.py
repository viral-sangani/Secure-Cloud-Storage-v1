from django.urls import path, include
from account.api import RegisterAPI, UserAPI, FileUploadAPI, GetFilesAPI
from django.conf import settings
from django.conf.urls.static import static

# /api/auth/*
urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/user/',UserAPI.as_view()),
    path('file/encrypt/', FileUploadAPI.as_view()),
    path('file/show/', GetFilesAPI.as_view()),
    
    # path('file/encrypt/', FileAPI.as_view())
]