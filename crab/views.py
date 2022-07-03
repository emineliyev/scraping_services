from django.shortcuts import render
from django.views.generic import ListView, FormView

from .forms import FindForm
from .models import Vacancy


# class IndexView(ListView):
#     model = Vacancy
#     template_name = 'crab/index.html'
#     context_object_name = 'crabs'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def index(request):
    form = FindForm
    city = request.GET.get('city')
    category = request.GET.get('category')
    crabs = []
    if city or category:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if category:
            _filter['category__slug'] = category

        crabs = Vacancy.objects.filter(**_filter)
    context = {
        'crabs': crabs,
        'form': form
    }
    return render(request, 'crab/index.html', context=context)



