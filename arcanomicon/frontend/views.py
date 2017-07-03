from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views import generic

from core.models import AddOn, AddOnVersion
from frontend.forms import AddOnForm, AddOnPageForm, AddOnVersionForm


class IndexView(generic.ListView):
    template_name = 'frontend/addon_list.html'
    queryset = AddOn.objects.all().order_by('-updated')[:10]
    context_object_name = 'add_ons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_wow_version'] = current_wow_version()
        return context


class DetailView(generic.DetailView):
    template_name = 'frontend/addon_details.html'
    model = AddOn
    context_object_name = 'add_on'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_wow_version'] = current_wow_version()
        return context


class SearchView(generic.ListView):
    template_name = 'frontend/addon_list.html'
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


class AddOnCreateView(View):
    template_name = 'frontend/addon_form.html'

    def post(self, request):
        add_on_form = AddOnForm(request.POST, request.FILES)
        page_form = AddOnPageForm(request.POST)

        if add_on_form.is_valid() and page_form.is_valid():
            add_on_form.instance.creator = request.user.user
            add_on_form.instance.page = page_form.instance
            add_on = add_on_form.save()
            page_form.instance.add_on = add_on
            page_form.save()

            return redirect(add_on.get_absolute_url())

        return render(request, self.template_name, context={
            'add_on_form': add_on_form,
            'page_form': page_form,
        })

    def get(self, request):
        add_on_form = AddOnForm()
        page_form = AddOnPageForm()

        return render(request, self.template_name, context={
            'add_on_form': add_on_form,
            'page_form': page_form,
        })


class AddOnVersionCreateView(View):
    template_name = 'frontend/addon_version_form.html'

    def post(self, request, slug, pk):
        add_on = get_object_or_404(AddOn, pk=pk)
        if request.user.user.pk != add_on.creator.pk:
            raise PermissionError()

        form = AddOnVersionForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.add_on = add_on
            form.save()
            return redirect(form.instance.add_on)

        return render(request, self.template_name, context={
            'form': form,
            'add_on': add_on,
        })

    def get(self, request, slug, pk):
        add_on = get_object_or_404(AddOn, pk=pk)
        if request.user.user.pk != add_on.creator.pk:
            raise PermissionError()

        form = AddOnVersionForm()

        return render(request, self.template_name, context={
            'form': form,
            'add_on': add_on,
        })


def current_wow_version():
    from arcanomicon import settings

    return settings.CURRENT_WOW_VERSION