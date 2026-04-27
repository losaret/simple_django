# user_profile/signals.py
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from .models import ExtendUser
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)


User = get_user_model()
logger = logging.getLogger("user_profile")


def _mask_identifier(value: str | None, max_visible: int = 2) -> str | None:
    """
    Маскирует логин/email в логах:
    - первые max_visible символов оставляем,
    - остальное заменяем звездочками,
    - домен email не трогаем.
    """
    if not value:
        return None

    if "@" in value:
        local, domain = value.split("@", 1)
        if len(local) <= max_visible:
            return "*" * len(local) + "@" + domain
        return local[:max_visible] + "*" * (len(local) - max_visible) + "@" + domain

    # обычный логин без @
    if len(value) <= max_visible:
        return "*" * len(value)
    return value[:max_visible] + "*" * (len(value) - max_visible)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtendUser.objects.create(user=instance)
        EmailAddress.objects.create(user=instance, email=instance.email, primary=True)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    ua = request.META.get("HTTP_USER_AGENT", "")
    logger.info(
        "LOGIN_SUCCESS  id=%s ip=%s ua=%s",
        user.pk,
        ip,
        ua,
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    ua = request.META.get("HTTP_USER_AGENT", "")
    logger.info(
        "LOGOUT_SUCCESS  id=%s ip=%s ua=%s",
        getattr(user, "pk", None),
        ip,
        ua,
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    raw_identifier = credentials.get("username")
    masked_identifier = _mask_identifier(raw_identifier)
    ip = request.META.get("REMOTE_ADDR") if request else None
    ua = request.META.get("HTTP_USER_AGENT", "") if request else None
    logger.warning(
        "LOGIN_FAILED identifier=%s ip=%s ua=%s",
        masked_identifier,
        ip,
        ua,
    )