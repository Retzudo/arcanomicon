from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic

from core.models import AddOn


class IndexView(generic.ListView):
    template_name = 'frontend/index.html'
    queryset = AddOn.objects.all().order_by('-updated')[:10]
    context_object_name = 'add_ons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_wow_version'] = current_wow_version()
        return context


class DetailView(generic.DetailView):
    template_name = 'frontend/details.html'
    model = AddOn
    context_object_name = 'add_on'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_wow_version'] = current_wow_version()
        return context


class SearchView(generic.ListView):
    template_name = 'frontend/index.html'
    context_object_name = 'add_ons'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return AddOn.objects.none()

        return AddOn.objects.filter(Q(name__contains=query.lower()) | Q(short_description__contains=query.lower()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_wow_version'] = current_wow_version()
        return context


def current_wow_version():
    from arcanomicon import settings

    return settings.CURRENT_WOW_VERSION