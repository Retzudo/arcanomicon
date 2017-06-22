from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from core.models import User, AddOn, AddOnPage, AddOnVersion


@receiver(post_save, sender=DjangoUser)
def create_user(sender, instance, created, **kwargs):
    """Create an Arcanomicon User object for every Django User."""
    if created:
        User.objects.get_or_create(user=instance)


@receiver(post_save, sender=AddOn)
def create_add_on_page(sender, instance, created, **kwargs):
    """Create an add-on page for every add-on"""
    if created and not instance.page:
        AddOnPage.objects.get_or_create(add_on=instance)


@receiver(post_save, sender=AddOnVersion)
def update_add_on_timestamp(sender, instance, created, **kwargs):
    """Update the timestamp on an add-on after a version was added."""
    if created:
        # Trigger an update on the Add-on's `updated` property
        instance.add_on.save()