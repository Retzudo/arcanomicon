from django.conf.urls import url, include

from api import views

urlpatterns = [
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'favourites/$', views.FavouritesView.as_view()),
    url(r'favourites/(?P<add_on_id>\d+)$', views.FavouritesView.as_view()),
]
