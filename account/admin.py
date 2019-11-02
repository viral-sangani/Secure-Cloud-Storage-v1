from django.contrib import admin
from account.models import Key, encrypted_storage

# Register your models here.
admin.site.register(Key)
admin.site.register(encrypted_storage)
