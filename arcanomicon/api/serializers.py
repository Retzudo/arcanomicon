from rest_framework import serializers

from core import models


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddOn
        fields = '__all__'