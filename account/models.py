from django.db import models
from django.contrib.auth.models import User

class Key(models.Model):
    private_key = models.TextField()
    public_key= models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "keys"
    
    def __str__(self):
        return self.user.username


class encrypted_storage(models.Model):
    encrypted_blob = models.BinaryField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=15000)
    size = models.CharField(max_length=150)
    ext = models.CharField(max_length=100)

    class Meta:
        db_table = "encrypted_storage"