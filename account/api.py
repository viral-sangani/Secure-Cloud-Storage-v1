from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializers import  RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from account.Encryption.generate_RSA_key import generate
from account.Encryption.RSA_encrypt import encrypt_blob
from account.models import Keys, encrypted_storage
from django.core.files.base import ContentFile
import base64
from django.forms.models import model_to_dict

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_token = User.objects.get(username=request.data['username'])
        private, public = generate()
        Keys.objects.create(
            private_key=private,
            public_key=public,
            user=user_token
        )
        return Response({
            'user': model_to_dict(user_token, fields=['id', 'username', 'email']),
        })

class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request._user:
            return Response(User.objects.get(pk=request._user.pk))
        else:
            return Response({"Error":"Please Login"})


class FileAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file = request.data['file']
        key = Keys.objects.get(user=request.user)
        unencrypted_blob = file.read()
        public_key = key.public_key
        encrypted_blob = encrypt_blob(unencrypted_blob, public_key)
        temp = encrypted_storage()
        temp.user = request.user
        temp.encrypted_blob = ContentFile(base64.b64decode(encrypted_blob), name="temp.jpg")
        temp.save()
        return Response({"Success":"Image Received"})

class GetFilesAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        res = []
        count = 1
        for item in encrypted_storage.objects.filter(user=request.user):
            res.append({count:{"path": item.encrypted_blob.url, "name": item.encrypted_blob.name}})
            count += 1
        return Response(res)
        