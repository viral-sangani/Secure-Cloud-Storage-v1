from django.contrib import admin
from account.models import Keys, encrypted_storage

# Register your models here.
admin.site.register(Keys)
admin.site.register(encrypted_storage)
