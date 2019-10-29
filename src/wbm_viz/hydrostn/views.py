from django.shortcuts import render
from .models import Hydrostn30Subbasin
# Create your views here.
def index(request):
    count_subbasin = Hydrostn30Subbasin.objects.count()
    subbasin = Hydrostn30Subbasin.objects.filter(id=1).first()
    catchment = subbasin.get_catchment()


    context = {
        'count_subbasin': count_subbasin,
        'subbasin': subbasin,
        'catchment': catchment,
    }

    return render(request, 'index.html', context)