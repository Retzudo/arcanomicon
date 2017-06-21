from django.shortcuts import render

from arcanomicon import settings
from core.models import AddOn


def index(request):
    recent_add_ons = AddOn.objects.all().order_by('-updated')[:10]
    return render(request, 'frontend/index.html', context={
        'add_ons': recent_add_ons,
        'current_wow_version': settings.CURRENT_WOW_VERSION,
    })
