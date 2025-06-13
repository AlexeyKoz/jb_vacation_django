from django.shortcuts import render
from django.views.generic import TemplateView
from apps.vacations.models import Vacation

# Create your views here.


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacations'] = Vacation.objects.all().order_by('-created_at')
        return context
