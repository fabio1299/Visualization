from django.shortcuts import render
from django.views import View
from .models import Hydrostn30Subbasin
# Create your views here.

class SubbasinView(View):

    template_name = 'subbasin.html'


    def get(self,request,subbasin_id,*args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        # polygon styling
        polygon_style = {
                            'sub_border': 'red', 'sub_fill': '#3333FF',
                            'catch_border': '#00FFFF', 'catch_fill': '#33BBFF',
                         }

        context = {'subbasin': subbasin, 'polygon_style': polygon_style}
        return render(request, self.template_name, context=context)

