from django.shortcuts import render
from django.views import View

from .models import ArgentinaHydrostn30Subbasin, ArgentinaHydrostn30Streamline, \
    ArgentinaCatchmentStatsEvapotranspiration, \
    ArgentinaCatchmentStatsRunoff, ArgentinaCatchmentStatsPrecipitation, ArgentinaCatchmentStatsSoilMoisture, \
    ArgentinaCatchmentBasins, \
    ArgentinaCatchmentStatsAirTemperature, ArgentinaSubbasinAirTemperatureMonthly, \
    ArgentinaSubbasinEvapotranspirationMonthly, \
    ArgentinaSubbasinPrecipitationMonthly, ArgentinaSubbasinRunoffMonthly, ArgentinaSubbasinSoilMoistureMonthly, \
    ArgentinaConfluenceDischargeMonthly

from .models import PeruHydrostn30Subbasin, PeruHydrostn30Streamline, PeruCatchmentStatsEvapotranspiration, \
    PeruCatchmentStatsRunoff, PeruCatchmentStatsPrecipitation, PeruCatchmentStatsSoilMoisture, PeruCatchmentBasins, \
    PeruCatchmentStatsAirTemperature, PeruSubbasinAirTemperatureMonthly, PeruSubbasinEvapotranspirationMonthly, \
    PeruSubbasinPrecipitationMonthly, PeruSubbasinRunoffMonthly, PeruSubbasinSoilMoistureMonthly, \
    PeruConfluenceDischargeMonthly

from . import geometry, db_routines
from .tasks import plot_queryset, my_task

SUBBASIN = {'argentina': ArgentinaHydrostn30Subbasin, 'peru': PeruHydrostn30Subbasin}
STREAMLINE = {'argentina': ArgentinaHydrostn30Streamline, 'peru': PeruHydrostn30Streamline}
CATCHMENT_BASINS = {'argentina': ArgentinaCatchmentBasins, 'peru': PeruCatchmentBasins}
DISCHARGE = {'argentina': ArgentinaConfluenceDischargeMonthly, 'peru': PeruConfluenceDischargeMonthly}
CATCHMENT_STATS_EVAP = {'argentina': ArgentinaCatchmentStatsEvapotranspiration,
                        'peru': PeruCatchmentStatsEvapotranspiration}
CATCHMENT_STATS_RUNOFF = {'argentina': ArgentinaCatchmentStatsRunoff, 'peru': PeruCatchmentStatsRunoff}
CATCHMENT_STATS_PRECIP = {'argentina': ArgentinaCatchmentStatsPrecipitation, 'peru': PeruCatchmentStatsPrecipitation}
CATCHMENT_STATS_SOIL = {'argentina': ArgentinaCatchmentStatsSoilMoisture, 'peru': PeruCatchmentStatsSoilMoisture}
CATCHMENT_STATS_AIR = {'argentina': ArgentinaCatchmentStatsAirTemperature, 'peru': PeruCatchmentStatsAirTemperature}
SUBBASIN_STATS_EVAP = {'argentina': ArgentinaSubbasinEvapotranspirationMonthly,
                       'peru': PeruSubbasinEvapotranspirationMonthly}
SUBBASIN_STATS_RUNOFF = {'argentina': ArgentinaSubbasinRunoffMonthly, 'peru': PeruSubbasinRunoffMonthly}
SUBBASIN_STATS_PRECIP = {'argentina': ArgentinaSubbasinPrecipitationMonthly, 'peru': PeruSubbasinPrecipitationMonthly}
SUBBASIN_STATS_SOIL = {'argentina': ArgentinaSubbasinSoilMoistureMonthly, 'peru': PeruSubbasinSoilMoistureMonthly}
SUBBASIN_STATS_AIR = {'argentina': ArgentinaSubbasinAirTemperatureMonthly, 'peru': PeruSubbasinAirTemperatureMonthly}


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, subbasin_id=1, country='argentina', *args, **kwargs):

        # Map
        subbasin_count = SUBBASIN[country].objects.count()
        subbasin = SUBBASIN[country].objects.filter(id=subbasin_id).first()
        catch_cache = CATCHMENT_BASINS[country].objects.filter(sample_id=subbasin_id).first()
        stream = STREAMLINE[country].objects.filter(id__in=catch_cache.basins)

        if catch_cache.catchment == None:
            # call proc to gen table from DB
            catch_table = db_routines.get_catchment_table(subbasin, country, '01min')

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
            qs = model.objects.filter(subbasin_id=subbasin_id).order_by('subbasin_id', 'date')

            result = plot_queryset.delay(list(qs.values()), ['Terraclimate', 'WBMprist_CRUTSv401', 'WBMprist_GPCCv7'],
                                         y_param, title=title)
            return result

        discharge = trigger_plot(DISCHARGE[country], y_param='discharge', title='Basin Monthly Discharge')

        evap_basin = trigger_plot(SUBBASIN_STATS_EVAP[country], y_param='zonal_mean',
                                  title="Basin Mean Evapotranspiration")
        air_basin = trigger_plot(SUBBASIN_STATS_AIR[country], y_param='zonal_mean',
                                 title="Basin Mean Air Temperature")
        precip_basin = trigger_plot(SUBBASIN_STATS_PRECIP[country], y_param="zonal_mean",
                                    title="Basin Mean Precipitation")
        runoff_basin = trigger_plot(SUBBASIN_STATS_RUNOFF[country], y_param="zonal_mean", title="Basin Mean Runoff")
        soil_basin = trigger_plot(SUBBASIN_STATS_SOIL[country], y_param="zonal_mean", title="Basin Mean Soil Moisture")

        evap_catch = trigger_plot(CATCHMENT_STATS_EVAP[country], title="Catchment Mean Evapotranspiration")
        air_catch = trigger_plot(CATCHMENT_STATS_AIR[country], title="Catchment Mean Air Temperature")
        precip_catch = trigger_plot(CATCHMENT_STATS_PRECIP[country], title="Catchment Mean Precipitation")
        runoff_catch = trigger_plot(CATCHMENT_STATS_RUNOFF[country], title="Catchment Mean Runoff")
        soil_catch = trigger_plot(CATCHMENT_STATS_SOIL[country], title="Catchment Mean Soil Moisture")

        context = {'country': country, 'subbasin_count': subbasin_count,
            'subbasin_id': subbasin_id, 'subbasin': subbasin, 'catch_geom': catch_geom,
            'stream_geom': stream_geom, 'evap_catch_task_id': evap_catch.task_id,
            'air_catch_task_id': air_catch.task_id, 'precip_catch_task_id': precip_catch.task_id,
            'runoff_catch_task_id': runoff_catch.task_id, 'soil_catch_task_id': soil_catch.task_id,
            'evap_basin_task_id': evap_basin.task_id, 'air_basin_task_id': air_basin.task_id,
            'precip_basin_task_id': precip_basin.task_id, 'runoff_basin_task_id': runoff_basin.task_id,
            'soil_basin_task_id': soil_basin.task_id, 'discharge_task_id': discharge.task_id
        }
        return render(request, self.template_name, context=context)
