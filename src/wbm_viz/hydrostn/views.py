from django.shortcuts import render
from django.views import View
from .models import Hydrostn30Subbasin, Hydrostn30Streamline, CatchmentStatsEvapotranspiration, \
    CatchmentStatsRunoff, CatchmentStatsPrecipitation, CatchmentStatsSoilMoisture, CatchmentBasins, \
    CatchmentStatsAirTemperature, SubbasinAirTemperatureMonthly, SubbasinEvapotranspirationMonthly, \
    SubbasinPrecipitationMonthly, SubbasinRunoffMonthly, SubbasinSoilMoistureMonthly, ConfluenceDischargeMonthly
from . import geometry, db_routines
from .tasks import plot_queryset, my_task


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, subbasin_id=1, *args, **kwargs):

        # Map
        subbasin = Hydrostn30Subbasin.objects.filter(id=subbasin_id).first()
        catch_cache = CatchmentBasins.objects.filter(sample_id=subbasin_id).first()
        stream = Hydrostn30Streamline.objects.filter(id__in=catch_cache.basins)

        if catch_cache.catchment == None:
            # call proc to gen table from DB
            catch_table = db_routines.get_catchment_table(subbasin)

            # collect all geom
            catch_collection = geometry.get_geometrycollection(catch_table)
            stream_collection = geometry.get_geometrycollection(stream.values())

            # union all geom
            catch_geom = catch_collection.unary_union
            stream_geom = stream_collection.unary_union

        else:
            # use cached geometry (too big to compute on fly)
            catch_geom = catch_cache.catchment
            stream_geom = catch_cache.streamlines

        # Plots
        def trigger_plot(model, title=None, y_param='mean_zonal_mean'):
            qs = model.objects.filter(subbasin_id=subbasin_id)

            result = plot_queryset.delay(list(qs.values()), ['Terraclimate', 'WBMprist_CRUTSv401', 'WBMprist_GPCCv7'],
                                         y_param, title=title)
            return result

        discharge = trigger_plot(ConfluenceDischargeMonthly, y_param='discharge', title='Basin Monthly Discharge')

        evap_basin = trigger_plot(SubbasinEvapotranspirationMonthly, y_param='zonal_mean',
                                  title="Basin Mean Evapotranspiration")
        air_basin = trigger_plot(SubbasinAirTemperatureMonthly, y_param='zonal_mean',
                                 title="Basin Mean Air Temperature")
        precip_basin = trigger_plot(SubbasinPrecipitationMonthly, y_param="zonal_mean",
                                    title="Basin Mean Precipitation")
        runoff_basin = trigger_plot(SubbasinRunoffMonthly, y_param="zonal_mean", title="Basin Mean Runoff")
        soil_basin = trigger_plot(SubbasinSoilMoistureMonthly, y_param="zonal_mean", title="Basin Mean Soil Moisture")

        evap_catch = trigger_plot(CatchmentStatsEvapotranspiration, title="Catchment Mean Evapotranspiration")
        air_catch = trigger_plot(CatchmentStatsAirTemperature, title="Catchment Mean Air Temperature")
        precip_catch = trigger_plot(CatchmentStatsPrecipitation, title="Catchment Mean Precipitation")
        runoff_catch = trigger_plot(CatchmentStatsRunoff, title="Catchment Mean Runoff")
        soil_catch = trigger_plot(CatchmentStatsSoilMoisture, title="Catchment Mean Soil Moisture")

        context = {
            'subbasin_id': subbasin_id, 'subbasin': subbasin, 'catch_geom': catch_geom,
            'stream_geom': stream_geom, 'evap_catch_task_id': evap_catch.task_id,
            'air_catch_task_id': air_catch.task_id, 'precip_catch_task_id': precip_catch.task_id,
            'runoff_catch_task_id': runoff_catch.task_id, 'soil_catch_task_id': soil_catch.task_id,
            'evap_basin_task_id': evap_basin.task_id, 'air_basin_task_id': air_basin.task_id,
            'precip_basin_task_id': precip_basin.task_id, 'runoff_basin_task_id': runoff_basin.task_id,
            'soil_basin_task_id': soil_basin.task_id, 'discharge_task_id': discharge.task_id
        }
        return render(request, self.template_name, context=context)
