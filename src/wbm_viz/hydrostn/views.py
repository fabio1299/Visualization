from django.shortcuts import render
from .models import Hydrostn30Subbasin
# Create your views here.
def index(request):
    count_subbasin = Hydrostn30Subbasin.objects.count()

    context = {
        'count_subbasin': count_subbasin,
    }

    return render(request, 'index.html', context)