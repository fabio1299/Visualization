from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Hydrostn30Subbasin, CatchmentStatsAirTemperature, CatchmentStatsEvapotranspiration, \
    CatchmentStatsRunoff, CatchmentStatsPrecipitation, CatchmentStatsSoilMoisture
import pandas as pd
from . import geometry, db_routines
from wbm_viz.graphql import run_query, query_model_stats_monthly, query_to_df

#plotting
import plotly
import plotly.graph_objects as go
import json

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
        # subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()

        evapotranspiration = CatchmentStatsEvapotranspiration.objects.filter(subbasin_id=subbasin_id)
        # air_temperature = CatchmentStatsAirTemperature.objects.filter(subbasin_id=subbasin_id)
        # runoff = CatchmentStatsRunoff.objects.filter(subbasin_id=subbasin_id)
        # precipitation = CatchmentStatsPrecipitation.objects.filter(subbasin_id=subbasin_id)
        # soil_moisture = CatchmentStatsSoilMoisture.objects.filter(subbasin_id=subbasin_id)

        df_evapotranspiration = pd.DataFrame(evapotranspiration.values())

        data = [
            go.Scattergl(
                x=df_evapotranspiration['date'],
                y=df_evapotranspiration['mean_zonal_mean'],
            )
        ]

        layout = go.Layout(
            title='Evapotranspiration',
        )

        fig = go.Figure(data=data, layout=layout)

        plt_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        context = {'subbasin_id': subbasin_id, 'plt_json':plt_json}
        return render(request,self.template_name,context=context)
