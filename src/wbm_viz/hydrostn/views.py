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
from .tasks import plot_queryset

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

UNITS = {
    'discharge': 'm<sup>3</sup>/s',
    'temp': '&#8451;',
    'evap': 'mm/month',
    'precip': 'mm/month',
    'runoff': 'mm/month',
    'soil': 'mm/month'
}
from timeit import default_timer as timer

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
            #catch_table = db_routines.get_catchment_table(subbasin, country, '01min')
            catch_table = db_routines.get_catchment_subbasins(subbasin.id, country, '01min')

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
        def trigger_plot(model, title=None, units=None, y_param='mean_zonal_mean'):
            qs_ids = model.objects.filter(subbasin_id=subbasin_id).values_list('id', flat=True)
            model_name = model.__name__
            result = plot_queryset.delay(model_name, list(qs_ids), ['Terraclimate', 'WBMprist_CRUTSv401', 'WBMprist_GPCCv7'],
                                         y_param, title=title, units=units)
            return result

        discharge = trigger_plot(DISCHARGE[country], y_param='discharge', title='Basin Monthly Discharge',units=UNITS['discharge'])

        evap_basin = trigger_plot(SUBBASIN_STATS_EVAP[country], y_param='zonal_mean',
                                  title="Basin Mean Evapotranspiration",units=UNITS['evap'])
        air_basin = trigger_plot(SUBBASIN_STATS_AIR[country], y_param='zonal_mean',
                                 title="Basin Mean Air Temperature",units=UNITS['temp'])
        precip_basin = trigger_plot(SUBBASIN_STATS_PRECIP[country], y_param="zonal_mean",
                                    title="Basin Mean Precipitation",units=UNITS['precip'])
        runoff_basin = trigger_plot(SUBBASIN_STATS_RUNOFF[country], y_param="zonal_mean", title="Basin Mean Runoff",units=UNITS['runoff'])
        soil_basin = trigger_plot(SUBBASIN_STATS_SOIL[country], y_param="zonal_mean", title="Basin Mean Soil Moisture", units=UNITS['soil'])

        evap_catch = trigger_plot(CATCHMENT_STATS_EVAP[country], title="Catchment Mean Evapotranspiration", units=UNITS['evap'])
        air_catch = trigger_plot(CATCHMENT_STATS_AIR[country], title="Catchment Mean Air Temperature",units=UNITS['temp'])
        precip_catch = trigger_plot(CATCHMENT_STATS_PRECIP[country], title="Catchment Mean Precipitation", units=UNITS['precip'])
        runoff_catch = trigger_plot(CATCHMENT_STATS_RUNOFF[country], title="Catchment Mean Runoff", units=UNITS['runoff'])
        soil_catch = trigger_plot(CATCHMENT_STATS_SOIL[country], title="Catchment Mean Soil Moisture", units=UNITS['soil'])

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

from django.http import HttpResponse
from .db_routines import get_container_geometry
from django.shortcuts import redirect

def StationRedirect(request, country=None, lat=None, lon=None):
    subbasin_id = get_container_geometry(float(lon), float(lat), SUBBASIN[country])
    if not subbasin_id:
        return(HttpResponse('ERROR: lat={},lon={} not found in {}'.format(lat,lon,country)))
    else:
        return redirect('home', subbasin_id=subbasin_id.first().id, country=country)
