from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class status(models.TextChoices):
    vkusno = 'vk', 'vkusno'
    nevkusno = 'ne', 'nevkusno'
    
class categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class product_card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('created_date', default=timezone.now)
    comment = models.CharField(blank=False, max_length=160)
    upload_url = str('mediafiles/')
    card_image = models.ImageField(upload_to=upload_url)
    choice = models.CharField(
        max_length=2,
        choices=status.choices,
    )
    category = models.ForeignKey(categories, on_delete=models.CASCADE)

    
