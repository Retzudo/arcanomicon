from django.shortcuts import render

from core.models import AddOn


def index(request):
    recent_add_ons = AddOn.objects.all().order_by('-updated')[:10]
    return render(request, 'frontend/index.html', context={
        'add_ons': recent_add_ons
    })
