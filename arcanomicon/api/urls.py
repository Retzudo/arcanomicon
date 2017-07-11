from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'addons', views.AddOnViewSet, base_name='addons')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'favourites/$', views.FavouritesView.as_view()),
    url(r'favourites/(?P<add_on_id>\d+)$', views.FavouritesView.as_view()),
    url(r'addons/(?P<add_on_id>\d+)/versions/(?P<version_id>\d+)$', views.DeleteAddOnVersion.as_view())
]
