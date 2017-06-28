# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 07:56
from __future__ import unicode_literals

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'Add-on',
            },
        ),
        migrations.CreateModel(
            name='AddOnPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_description', models.TextField()),
                ('add_on', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='page', to='core.AddOn')),
            ],
            options={
                'verbose_name': 'Add-on page',
            },
        ),
        migrations.CreateModel(
            name='AddOnVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255)),
                ('supports', models.CharField(choices=[('7.2.5', '7.2.5'), ('7.2.0', '7.2.0'), ('7.1.5', '7.1.5'), ('7.1.0', '7.1.0')], max_length=8)),
                ('file', models.FileField(upload_to=core.models.upload_to)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('add_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='core.AddOn')),
            ],
            options={
                'verbose_name': 'Add-on version',
                'ordering': ('-added',),
            },
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('add_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='core.AddOn')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourites', models.ManyToManyField(related_name='favourited_by', to='core.AddOn')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='addon',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='contributes_to', to='core.User'),
        ),
        migrations.AddField(
            model_name='addon',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addons_created', to='core.User'),
        ),
    ]
