from django.db.models import Q
from django.views import generic

from core.models import AddOn, AddOnPage
from frontend.forms import AddOnForm


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


class AddOnCreate(generic.CreateView):
    model = AddOn
    form_class = AddOnForm
    template_name = 'frontend/addon_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user.user
        form.instance.page = AddOnPage(long_description=form.cleaned_data['long_description'])
        return super(AddOnCreate, self).form_valid(form)


def current_wow_version():
    from arcanomicon import settings

    return settings.CURRENT_WOW_VERSION