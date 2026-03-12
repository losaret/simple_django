from django.contrib import admin

# Register your models here.
from .models import ExtendUser

admin.site.register(ExtendUser)