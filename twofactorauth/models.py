from django.db import models
from django.contrib.auth.models import User

class Twofactorauth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Twofactorauth'

    def __str__(self):
        return self.user.username + " - " + str(self.otp)

# Create your models here.
