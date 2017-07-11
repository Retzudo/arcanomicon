from django.db.models import Q
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from api import serializers
from core.models import AddOn


class AddOnViewSet(viewsets.ModelViewSet):
    """List all add-ons."""
    serializer_class = serializers.AddOnSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Allow a `q` paramter for searching."""
        query = self.request.query_params.get('q')

        if query:
            return AddOn.objects.filter(Q(name__contains=query.lower()) | Q(short_description__contains=query.lower()))
        else:
            return AddOn.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.user)


class FavouritesView(ListAPIView, CreateModelMixin, DestroyModelMixin, GenericAPIView):
    """List all favourites for a user."""
    serializer_class = serializers.AddOnSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.user.favourites.all()

    def post(self, request):
        """Add an existing add-on to the current user's favourites list."""
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
        """Remove an add-on from the current user's list."""
        try:
            add_on = request.user.user.favourites.get(pk=add_on_id)
        except AddOn.DoesNotExist:
            raise ValidationError('Add-on not favourited')

        request.user.user.favourites.remove(add_on)

        return Response('', status=204)


class DeleteAddOnVersion(DestroyModelMixin, GenericAPIView):
    """Delete a version of an add-on.

    Only the add-on's creator is allowed to delete versions."""
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, add_on_id, version_id):
        add_on = get_object_or_404(AddOn, pk=add_on_id)
        version = add_on.versions.get(pk=version_id)

        if add_on.creator.pk != request.user.user.pk:
            # Only the add-on's creator is allowed to delete versions.
            raise PermissionError()

        version.delete()

        return Response('', status=204)
