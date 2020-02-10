from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Hydrostn30Subbasin, CatchmentStatsAirTemperature, CatchmentStatsEvapotranspiration, \
    CatchmentStatsRunoff, CatchmentStatsPrecipitation, CatchmentStatsSoilMoisture
from . import geometry, db_routines
from wbm_viz.graphql import run_query, query_model_stats_monthly, query_to_df
from .tasks import plot_queryset, my_task
import pandas as pd

# Create your views here.
def index(request):
    return render(request, 'home.html')

class SubbasinView(View):

    template_name = 'subbasin.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        # call proc to gen table from DB
        catch_table = db_routines.get_catchment_table(subbasin)

        # collect all subbasin geom
        catch_collection = geometry.get_geometrycollection(catch_table)

        # document subbasin ids composing catchment
        catch_df = pd.DataFrame(catch_table)
        catch_ids = catch_df.id.tolist()

        # union all geom
        catch_geom = catch_collection.unary_union
        # polygon styling
        polygon_style = {
                            'sub_border': 'red', 'sub_fill': '#3333FF',
                            'catch_border': '#00FFFF', 'catch_fill': '#33BBFF',
                         }

        context = {'subbasin': subbasin, 'catch_geom': catch_geom, 'catch_ids': catch_ids, 'polygon_style': polygon_style}
        return render(request, self.template_name, context=context)


class Subbasin2View(View):
    template_name = 'subbasin2.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):


        def trigger_plot(model):
            qs = model.objects.filter(subbasin_id=subbasin_id)

            result = plot_queryset.delay(list(qs.values()),['Terraclimate','WBMprist_CRUTSv401','WBMprist_GPCCv7'])
            return result

        evap = trigger_plot(CatchmentStatsEvapotranspiration)
        air = trigger_plot(CatchmentStatsAirTemperature)
        precip = trigger_plot(CatchmentStatsPrecipitation)
        runoff = trigger_plot(CatchmentStatsRunoff)
        soil = trigger_plot(CatchmentStatsSoilMoisture)

        context = {'subbasin_id': subbasin_id, 'evap_task_id': evap.task_id,'air_task_id': air.task_id,
                   'precip_task_id':precip.task_id,'runoff_task_id':runoff.task_id,
                   'soil_task_id':soil.task_id}
        return render(request,self.template_name, context=context)
