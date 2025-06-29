from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

def get_upload_path(instance, filename):
    return 'mediafiles/{0}/{1}'.format(instance.user, filename)

# Create your models here.
class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    @property
    def is_email_verified(self):
        """Проверяет верификацию email через allauth"""
        return EmailAddress.objects.filter(
            user=self.user, 
            email=self.user.email,
            verified=True
        ).exists()