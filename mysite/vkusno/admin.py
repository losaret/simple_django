from django.contrib import admin

# Register your models here.
from .models import product_card, categories

admin.site.register(product_card)
admin.site.register(categories)