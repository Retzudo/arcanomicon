import os.path

from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.utils.text import slugify

wow_version = [
    ('7.2.5', '7.2.5')
]


def upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    new_filename = '{name}-{version}.{ext}'.format(
        name=slugify(instance.add_on.name),
        version=instance.version,
        ext=ext,
    )

    return '{}/{}'.format(instance.add_on.pk, new_filename)


class User(models.Model):
    """Extended User model."""
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class AddOn(models.Model):
    """Add-on model."""
    creator = models.ForeignKey(User, related_name='addons', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    contributors = models.ManyToManyField(User, related_name='contributes_to', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Add-on'


class AddOnPage(models.Model):
    """Model for a add-on page."""
    add_on = models.OneToOneField(AddOn, on_delete=models.CASCADE)
    long_description = models.TextField()

    def __str__(self):
        return 'Add-on page for "{}"'.format(self.add_on.name)

    class Meta:
        verbose_name = 'Add-on page'


class Image(models.Model):
    """Model for an image/screenshot of an add-on."""
    image = models.ImageField()
    add_on_for_screenshots = models.ForeignKey(AddOn, related_name='screenshots')
    add_on_for_description = models.ForeignKey(AddOn, related_name='description_images')

    def __str__(self):
        return str(self.image)


class AddOnVersion(models.Model):
    add_on = models.ForeignKey(AddOn, related_name='versions')
    version = models.CharField(max_length=255)
    supports = models.CharField(max_length=8, choices=wow_version)
    file = models.FileField(upload_to=upload_to)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} version {}'.format(self.add_on.name, self.version)

    class Meta:
        verbose_name = 'Add-on version'