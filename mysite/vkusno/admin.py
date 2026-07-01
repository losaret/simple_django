from django.contrib import admin

# Register your models here.
from .models import ProductCard, Category

admin.site.register(ProductCard)
admin.site.register(Category)