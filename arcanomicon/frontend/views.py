from django.shortcuts import render, get_object_or_404

from core.models import AddOn


def index(request):
    recent_add_ons = AddOn.objects.all().order_by('-updated')[:10]

    return render(request, 'frontend/index.html', context={
        'add_ons': recent_add_ons,
        'current_wow_version': current_wow_version()
    })


def details(request, slug, add_on_id):
    add_on = get_object_or_404(AddOn, pk=add_on_id)

    return render(request, 'frontend/details.html', context={
        'add_on': add_on,
        'current_wow_version': current_wow_version()
    })


def current_wow_version():
    from arcanomicon import settings

    return settings.CURRENT_WOW_VERSION