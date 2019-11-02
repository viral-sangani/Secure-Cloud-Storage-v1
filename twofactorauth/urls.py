from django.urls import path, include
from twofactorauth.api import GetCodeAPI


urlpatterns = [
    path('code/', GetCodeAPI.as_view()),
    path('', include('rest_auth.urls')),
]

