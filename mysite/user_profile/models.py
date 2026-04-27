from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

def get_upload_path(instance, filename):
    return 'mediafiles/{0}/{1}'.format(instance.user, filename)

# Create your models here.
class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    def follow(self, target_user):
        if self == target_user:
            raise ValueError('Нельзя подписаться на себя')
        follow, created = Follow.objects.get_or_create(
            follower=self,
            following=target_user
        )
        return created
    
    def unfollow(self, target_user):
        Follow.objects.filter(follower=self, following=target_user).delete()

    def is_following(self, target_user):
        return Follow.objects.filter(follower=self, following=target_user).exists()
    
    def get_followers(self):
        return ExtendUser.objects.filter(following_set__following=self)
    
    def get_following(self):
        return ExtendUser.objects.filter(followers_set__follower=self)

    @property
    def followers_count(self):
        return self.followers_set.count()

    @property
    def following_count(self): 
        return self.following_set.count()

    @property
    def is_email_verified(self):
        """Проверяет верификацию email через allauth"""
        return EmailAddress.objects.filter(
            user=self.user, 
            email=self.user.email,
            verified=True
        ).exists()
    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        ExtendUser,
        on_delete=models.CASCADE,
        related_name='following_set'
    )
    following = models.ForeignKey(
        ExtendUser,
        on_delete=models.CASCADE,
        related_name='followers_set'
    )
    created_date = models.DateTimeField('created_date', default=timezone.now)
    class Meta:
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower', 'following']),
            models.Index(fields=['following', '-created_date'])
        ]
        ordering = ['-created_date']
    
    def __str__(self):
        return f'{self.follower} подписан на {self.following}'