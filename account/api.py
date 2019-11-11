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
from account.Encryption.RSA_decrypt import decrypt_blob
from account.models import Key, encrypted_storage
from django.core.files.base import ContentFile
import base64, tempfile, os, random
from django.forms.models import model_to_dict
from rest_auth.views import LoginView, LogoutView
from twofactorauth.models import Twofactorauth
from rest_framework.renderers import MultiPartRenderer
from django.http import HttpResponse

class LoginAPI(LoginView):
    def get_response(self):

        if '2fa_token' in self.request._data:
            tfa_user_obj = Twofactorauth.objects.get(user=self.user)
            if str(tfa_user_obj.otp) == self.request._data['2fa_token']:
                original_response = super().get_response()
                res_dic = {"status":"success"}
                original_response.data.update(res_dic)
                return original_response
            else:
                return Response({'Error': 'Wrong OTP Entered. Please Try Again'})
        else:
            return Response({'Error': 'Please Provide TwoFactor Authentication'})

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_token = User.objects.get(username=request.data['username'])
        private, public = generate()
        Key.objects.create(
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


class FileUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file = request.data['file']
        print(file._name)
        key = Key.objects.get(user=request.user)
        unencrypted_blob = file.read()
        public_key = key.public_key

        encrypted_blob = encrypt_blob(unencrypted_blob, public_key)
        
        

        encrypt_obj = encrypted_storage()
        encrypt_obj.user = request.user
        encrypt_obj.encrypted_blob = encrypted_blob
        encrypt_obj.file_name = file._name
        encrypt_obj.size = file.size
        encrypt_obj.save()


        print(encrypt_obj.encrypted_blob)
        print(type(encrypt_obj.encrypted_blob))
        

        fp = open("en.txt","wb")
        fp.write(encrypted_blob)
        fp.close()


        private_key = key.private_key
        print(encrypt_obj.pk)
        print(len(encrypt_obj.encrypted_blob))
        # decrypted_blob = decrypt_blob(encrypt_obj.encrypted_blob, private_key)
        print("Done")
        return Response({"Success":"Image Received"})

class FileDownloadAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        file_id = request.data['id']

        decrypt_obj = encrypted_storage.objects.get(pk=file_id, user=request.user)
        print(decrypt_obj)
        key = Key.objects.get(user=request.user)


        private_key = key.private_key
        temp_name = "temp_"+str(random.randint(0,999999))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        


        decrypted_blob = decrypt_blob(decrypt_obj.encrypted_blob, private_key)
        file_path = BASE_DIR+"/media/tmp/"+temp_name+".jpg"
        download_path = "/media/tmp/"+temp_name+".jpg"
        fp = open(file_path,"wb")
        fp.write(decrypted_blob)
        fp.close()
        print(file_path)
        try:
            return Response({'path':download_path, 'file_name':temp_name})
        finally:
            print("File Send")


class GetFilesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        res = []
        count = 1
        for item in encrypted_storage.objects.filter(user=request.user):
            res.append({count:{ "name": item.file_name, "size": item.size, "id":item.pk}})
            count += 1
        return Response(res)
        