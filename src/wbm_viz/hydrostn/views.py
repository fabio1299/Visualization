from django.shortcuts import render
from django.views import View
from .models import Hydrostn30Subbasin
# Create your views here.
def index(request):
    subbasin = Hydrostn30Subbasin.objects.filter(id=1).first()
    catchment = subbasin.get_catchment()

    context = {
        'subbasin': subbasin,
        'catchment': catchment,
    }

    return render(request, 'index.html', context)

class SubbasinView(View):

    template_name = 'subbasin.html'


    def get(self,request,subbasin_id,*args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        context = {'subbasin': subbasin}
        return render(request, self.template_name, context=context)

