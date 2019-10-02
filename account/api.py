from rest_framework import generics
from rest_framework.response import Response
from account.serializers import  RegisterSerializer
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_token = User.objects.get(username=request.data['username'])

        return Response({
            'user': model_to_dict(user_token, fields=['id', 'username', 'email']),
        })
