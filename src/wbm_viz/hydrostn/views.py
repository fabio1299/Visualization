from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Hydrostn30Subbasin

from .stats import db_routines, geometry


# Create your views here.
def index(request):
    return render(request, 'home.html')

class SubbasinMapView(View):

    template_name = 'subbasin_map.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        # call proc to gen table from DB
        catch_table = db_routines.get_catchment_table(subbasin)

        # collect all subbasin geom
        catch_collection = geometry.get_geometrycollection(catch_table)

        # union all geom
        catch_geom = catch_collection.unary_union

        # polygon styling
        polygon_style = {
                            'sub_border': 'red', 'sub_fill': '#3333FF',
                            'catch_border': '#00FFFF', 'catch_fill': '#33BBFF',
                         }

        context = {'subbasin': subbasin, 'catch_geom': catch_geom, 'polygon_style': polygon_style}
        return render(request, self.template_name, context=context)

