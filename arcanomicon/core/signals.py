from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from core.models import User


@receiver(post_save, sender=DjangoUser, dispatch_uid='create_app_user')
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.get_or_create(user=instance)
