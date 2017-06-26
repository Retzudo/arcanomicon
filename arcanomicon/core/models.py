import os.path

from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

wow_versions = [
    ('7.2.5', '7.2.5'),
    ('7.2.0', '7.2.0'),
    ('7.1.5', '7.1.5'),
    ('7.1.0', '7.1.0'),
]


def upload_to(instance, filename):
    """Construct the upload path for uploaded add-on ZIPs."""
    _, ext = os.path.splitext(filename)
    new_filename = '{name}-{version}{ext}'.format(
        name=slugify(instance.add_on.name),
        version=instance.version,
        ext=ext,
    )

    return '{}/{}'.format(instance.add_on.pk, new_filename)


class User(models.Model):
    """Extended User model."""
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    favourites = models.ManyToManyField('AddOn', related_name='favourited_by')

    def __str__(self):
        return str(self.user)


class AddOn(models.Model):
    """Add-on model."""
    creator = models.ForeignKey(User, related_name='addons_created', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    contributors = models.ManyToManyField(User, related_name='contributes_to', blank=True)
    logo = models.ImageField()

    @property
    def latest_version(self):
        return self.versions.first()

    def get_absolute_url(self):
        return reverse('addon_details', kwargs={'pk': self.pk, 'slug': slugify(self.name)})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Add-on'


class AddOnPage(models.Model):
    """Model for a add-on page."""
    add_on = models.OneToOneField(AddOn, on_delete=models.CASCADE, related_name='page')
    long_description = models.TextField()

    def __str__(self):
        return 'Add-on page for "{}"'.format(self.add_on.name)

    class Meta:
        verbose_name = 'Add-on page'


class Screenshot(models.Model):
    """Model for an image/screenshot of an add-on."""
    add_on = models.ForeignKey(AddOn, related_name='screenshots')
    image = models.ImageField()

    def __str__(self):
        return str(self.image)


class AddOnVersion(models.Model):
    """Version for an add-on."""
    add_on = models.ForeignKey(AddOn, related_name='versions')
    version = models.CharField(max_length=255)
    supports = models.CharField(max_length=8, choices=wow_versions)
    file = models.FileField(upload_to=upload_to)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} version {}'.format(self.add_on.name, self.version)

    class Meta:
        verbose_name = 'Add-on version'
        ordering = ('-added',)
