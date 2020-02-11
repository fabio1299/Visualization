from django.shortcuts import render
from django.views import View
from .models import Hydrostn30Subbasin, Hydrostn30Streamline, CatchmentStatsEvapotranspiration, \
    CatchmentStatsRunoff, CatchmentStatsPrecipitation, CatchmentStatsSoilMoisture, CatchmentBasins, CatchmentStatsAirTemperature
from . import geometry, db_routines
from .tasks import plot_queryset, my_task


class SubbasinView(View):

    template_name = 'subbasin.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()
        catch_cache = CatchmentBasins.objects.filter(sample_id=subbasin_id).first()
        stream = Hydrostn30Streamline.objects.filter(id__in=catch_cache.basins).values()

        if catch_cache.catchment == None:
            # call proc to gen table from DB
            catch_table = db_routines.get_catchment_table(subbasin)

            # collect all geom
            catch_collection = geometry.get_geometrycollection(catch_table)
            stream_collection = geometry.get_geometrycollection(stream)

            # union all geom
            catch_geom = catch_collection.unary_union
            stream_geom = stream_collection.unary_union

        else:
            # use cached geometry (too big to compute on fly)
            catch_geom = catch_cache.catchment
            stream_geom = catch_cache.streamlines

        context = {'subbasin': subbasin, 'catch_geom': catch_geom, 'stream_geom': stream_geom,}
        return render(request, self.template_name, context=context)


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):

        # Map
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()
        catch_cache = CatchmentBasins.objects.filter(sample_id=subbasin_id).first()
        stream = Hydrostn30Streamline.objects.filter(id__in=catch_cache.basins).values()

        if catch_cache.catchment == None:
            # call proc to gen table from DB
            catch_table = db_routines.get_catchment_table(subbasin)

            # collect all geom
            catch_collection = geometry.get_geometrycollection(catch_table)
            stream_collection = geometry.get_geometrycollection(stream)

            # union all geom
            catch_geom = catch_collection.unary_union
            stream_geom = stream_collection.unary_union

        else:
            # use cached geometry (too big to compute on fly)
            catch_geom = catch_cache.catchment
            stream_geom = catch_cache.streamlines

        # Plots
        def trigger_plot(model):
            qs = model.objects.filter(subbasin_id=subbasin_id)

            result = plot_queryset.delay(list(qs.values()),['Terraclimate','WBMprist_CRUTSv401','WBMprist_GPCCv7'])
            return result

        evap = trigger_plot(CatchmentStatsEvapotranspiration)
        air = trigger_plot(CatchmentStatsAirTemperature)
        precip = trigger_plot(CatchmentStatsPrecipitation)
        runoff = trigger_plot(CatchmentStatsRunoff)
        soil = trigger_plot(CatchmentStatsSoilMoisture)

        context = {'subbasin_id': subbasin_id, 'subbasin': subbasin,'evap_task_id': evap.task_id,'air_task_id': air.task_id,
                   'precip_task_id':precip.task_id,'runoff_task_id':runoff.task_id,
                   'soil_task_id':soil.task_id, 'catch_geom': catch_geom,
                   'stream_geom': stream_geom}
        return render(request,self.template_name, context=context)
