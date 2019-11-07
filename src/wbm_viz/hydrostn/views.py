from django.shortcuts import render
from django.views import View
from .models import Hydrostn30Subbasin
# Create your views here.

class SubbasinView(View):

    template_name = 'subbasin.html'


    def get(self,request,subbasin_id,*args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        context = {'subbasin': subbasin}
        return render(request, self.template_name, context=context)

