from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random
from rest_framework.response import Response
from twofactorauth.models import Twofactorauth


class GetCodeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        otp = (random.randint(111111,999999))
        Twofactorauth.objects.filter(user=request.user).delete()
        Twofactorauth.objects.create(
            user=request.user,
            otp=otp
        )
        return Response({"otp":otp, "user":request.user.username})