import uuid

from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


def get_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return "mediafiles/{0}/{1}".format(instance.user, filename)


class Status(models.TextChoices):
    """
    Статус для карточки продукта
    """

    like = "lk", "like"
    dislike = "dl", "dislike"


class Category(models.Model):
    """
    Представляет категорию карточек, созданную пользователем.

    Attributes:
        name (CharField): Название категории (до 100 символов).
        user (ForeignKey): Владелец категории (связь с моделью User).
    """

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField("created_date", default=timezone.now)
    comment = models.CharField(blank=False, max_length=160)
    card_image = models.ImageField(upload_to=get_upload_path)
    choice = models.CharField(
        max_length=2,
        choices=Status.choices,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


auditlog.register(Category)
auditlog.register(ProductCard)


@receiver(post_delete, sender=ProductCard)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.card_image:
        instance.card_image.delete(save=False)


@receiver(pre_save, sender=ProductCard)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = sender.objects.get(pk=instance.pk).card_image
    except sender.DoesNotExist:
        return
    new_image = instance.card_image
    if old_image and old_image != new_image:
        old_image.delete(save=False)
