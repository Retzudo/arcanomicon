from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import serializers
from core.models import AddOn


class FavouritesView(ListAPIView, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    serializer_class = serializers.AddOnSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.user.favourites.all()

    def post(self, request):
        add_on_id = request.data.get('addOnId')
        if not add_on_id:
            raise ValidationError('addOnId missing')

        try:
            add_on = AddOn.objects.get(pk=add_on_id)
        except AddOn.DoesNotExist:
            raise ValidationError('Add-on not found')

        request.user.user.favourites.add(add_on)

        return Response('', status=201)

    def delete(self, request, add_on_id):
        try:
            add_on = request.user.user.favourites.get(pk=add_on_id)
        except AddOn.DoesNotExist:
            raise ValidationError('Add-on not favourited')

        request.user.user.favourites.remove(add_on)

        return Response('', status=204)
