from django.contrib import admin

# Register your models here.
from .models import ExtendUser, Follow

admin.site.register(ExtendUser)
admin.site.register(Follow)