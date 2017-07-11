from rest_framework import serializers

from core import models


class AddOnVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddOnVersion
        exclude = ('id',)


class AddOnSerializer(serializers.ModelSerializer):
    latest_version = AddOnVersionSerializer(read_only=True)
    long_description = serializers.CharField(required=False)

    class Meta:
        model = models.AddOn
        exclude = ('contributors', 'creator')
        depth = 1

    def create(self, validated_data):
        # Remove long_description from validated_data so django rest doesn't
        # try to create a new AddOn object with it. We only need it for creating
        # new AddOns via API.
        validated_data.pop('long_description')
        return super().create(validated_data)

