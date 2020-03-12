from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect

# All models & dictionaries mapping country to models
from .models import *

from . import geometry, db_routines
from .tasks import plot_queryset

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
            # catch_table = db_routines.get_catchment_table(subbasin, country, '01min')
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

        # Use ID set from discharge (chosen arbitrarily) to filter all statistic tables. We want to same set of IDS for all tables
        stat_subbasin_ids = list(DISCHARGE[country].objects.filter(subbasin_id=subbasin_id).values_list('subbasin_id', flat=True))

        # Plots
        def trigger_plot(model, title=None, units=None, y_param='mean_zonal_mean'):
            model_name = model.__name__
            result = plot_queryset.delay(model_name, stat_subbasin_ids, ['Terraclimate', 'WBMprist_CRUTSv401', 'WBMprist_GPCCv7'],
                                         y_param, title=title, units=units)
            return result

        discharge = trigger_plot(DISCHARGE[country], y_param='discharge', title='Basin Monthly Discharge',
                                 units=UNITS['discharge'])

        evap_basin = trigger_plot(SUBBASIN_STATS_EVAP[country], y_param='zonal_mean',
                                  title="Basin Mean Evapotranspiration", units=UNITS['evap'])
        air_basin = trigger_plot(SUBBASIN_STATS_AIR[country], y_param='zonal_mean',
                                 title="Basin Mean Air Temperature", units=UNITS['temp'])
        precip_basin = trigger_plot(SUBBASIN_STATS_PRECIP[country], y_param="zonal_mean",
                                    title="Basin Mean Precipitation", units=UNITS['precip'])
        runoff_basin = trigger_plot(SUBBASIN_STATS_RUNOFF[country], y_param="zonal_mean", title="Basin Mean Runoff",
                                    units=UNITS['runoff'])
        soil_basin = trigger_plot(SUBBASIN_STATS_SOIL[country], y_param="zonal_mean", title="Basin Mean Soil Moisture",
                                  units=UNITS['soil'])

        evap_catch = trigger_plot(CATCHMENT_STATS_EVAP[country], title="Catchment Mean Evapotranspiration",
                                  units=UNITS['evap'])
        air_catch = trigger_plot(CATCHMENT_STATS_AIR[country], title="Catchment Mean Air Temperature",
                                 units=UNITS['temp'])
        precip_catch = trigger_plot(CATCHMENT_STATS_PRECIP[country], title="Catchment Mean Precipitation",
                                    units=UNITS['precip'])
        runoff_catch = trigger_plot(CATCHMENT_STATS_RUNOFF[country], title="Catchment Mean Runoff",
                                    units=UNITS['runoff'])
        soil_catch = trigger_plot(CATCHMENT_STATS_SOIL[country], title="Catchment Mean Soil Moisture",
                                  units=UNITS['soil'])

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


def StationRedirect(request, country=None, lat=None, lon=None):
    subbasin_id = db_routines.get_container_geometry(float(lon), float(lat), SUBBASIN[country])
    if not subbasin_id:
        return (HttpResponse('ERROR: lat={},lon={} not found in {}'.format(lat, lon, country)))
    else:
        return redirect('home', subbasin_id=subbasin_id.first().id, country=country)
