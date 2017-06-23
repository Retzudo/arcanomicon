from django.conf.urls import url
from django.views.generic import TemplateView

from frontend import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^addon/(?P<slug>[-\w\d]+)-(?P<add_on_id>\d+)$', views.details, name='details'),
    url(r'^profile$', TemplateView.as_view(template_name='frontend/profile.html'), name='profile'),
    url(r'^search$', views.search, name='search'),
    url(r'^login$', auth_views.LoginView.as_view(template_name='frontend/login.html', redirect_authenticated_user=True), name='login'),
    url(r'^logout$', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    url(r'^$', views.index, name='index'),
]