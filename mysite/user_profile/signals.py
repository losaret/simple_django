# user_profile/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from .models import ExtendUser



User = get_user_model()

# def get_fake_request(user):
#     request = HttpRequest()
#     current_site = Site.objects.get_current()
#     request.META['HTTP_HOST'] = current_site.domain  # Например, 'example.com'
#     request.user = user
#     return request

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtendUser.objects.create(user=instance)
        EmailAddress.objects.create(user=instance, email=instance.email, primary=True)
