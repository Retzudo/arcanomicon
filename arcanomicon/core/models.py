from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    """Extended User model."""
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)


class AddOn(models.Model):
    """Add-on model."""
    creator = models.ForeignKey(User, related_name='addons', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=255)
    supports = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    contributors = models.ManyToManyField(User, related_name='contributes_to')


class AddOnPage(models.Model):
    """Model for a add-on page."""
    add_on = models.OneToOneField(AddOn, on_delete=models.CASCADE)
    long_description = models.TextField()


class Image(models.Model):
    """Model for an image/screenshot of an add-on."""
    image = models.ImageField()
    add_on_for_screenshots = models.ForeignKey(AddOn, related_name='screenshots')
    add_on_for_description = models.ForeignKey(AddOn, related_name='description_images')
