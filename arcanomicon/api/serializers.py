from rest_framework import serializers

from core import models


class AddOnVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddOnVersion
        exclude = ('id',)


class AddOnSerializer(serializers.ModelSerializer):
    latest_version = AddOnVersionSerializer(read_only=True)

    class Meta:
        model = models.AddOn
        exclude = ('contributors', 'creator')
        depth = 1
