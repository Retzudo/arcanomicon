from django.conf.urls import url

from frontend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'addon/(?P<slug>[-\w\d]+)-(?P<add_on_id>\d+)$', views.details, name='details'),
]