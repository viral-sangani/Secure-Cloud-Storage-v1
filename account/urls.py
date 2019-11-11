from django.urls import path, include
from account.api import RegisterAPI, UserAPI, FileUploadAPI, GetFilesAPI, LoginAPI, FileDownloadAPI
from django.conf import settings
from django.conf.urls.static import static
from rest_auth.urls import LogoutView

# /api/auth/*
urlpatterns = [
    # path('auth/', include('rest_auth.urls')),

    path('auth/login/', LoginAPI.as_view(), name="rest_login"),
    path('auth/logout/', LogoutView.as_view(), name="rest_logout"),
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/user/',UserAPI.as_view()),
    path('file/encrypt/', FileUploadAPI.as_view()),
    path('file/decrypt/', FileDownloadAPI.as_view()),
    path('file/show/', GetFilesAPI.as_view()),
    
    # path('file/encrypt/', FileAPI.as_view())
] 