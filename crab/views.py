from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import FindForm
from .models import Vacancy


def index(request):
    form = FindForm
    city = request.GET.get('city')
    category = request.GET.get('category')
    context = {'city': city, 'category': category, 'form': form}
    if city or category:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if category:
            _filter['category__slug'] = category

        crabs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(crabs, 7)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        context['crabs'] = page_obj
    return render(request, 'crab/index.html', context)



