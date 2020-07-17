from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import QxtWatertemp, NetworkWithGeometry
from django.core.serializers import serialize

from .tasks import plot_watertemp, watertemp_df, distance_plot, distance_plot_3d, avg_plot
from celery import chain,group

# Default change cache, may switch to more robust option later
from django.core.cache import cache

# Ajax test
from django.views.generic import FormView
from .forms import DataScopeForm, DistancePlotForm
from django.http import JsonResponse

from datetime import datetime
from pandas.tseries import offsets
from bs4 import BeautifulSoup

def get_cache_ids(network_id,start_year):
    result = {}
    start_year = str(start_year)
    end_year = start_year
    cache_id = '-'.join((str(network_id), start_year, end_year))
    result['df'] = cache_id + '-df'
    result['plot1'] = cache_id + '-p1'
    result['plot2'] = cache_id + '-p2'
    return result


def get_data(network_id,start_year):
    cache_dict = get_cache_ids(network_id,start_year)
    end_year = start_year

    result = {}
    ptm = NetworkWithGeometry.objects.filter(id=network_id).first().path_to_mouth()
    result['ptm'] = ptm

    # test celery task logic
    # df_json = watertemp_df(ptm,start_year,end_year)
    # p1 = avg_plot(df_json)
    # p2 = distance_plot(df_json,start_year,150)
    # p3 = distance_plot_3d(df_json,start_year)

    if cache.get(cache_dict['df']) is None:
        # Execute task chain
        # data is acquired from db into df
        # then piped into group of plotting tasks
        df_sig = watertemp_df.s(ptm, start_year, end_year)
        plot_tasks = group(avg_plot.s(), distance_plot_3d.s(start_year))
        plots = chain(df_sig, plot_tasks).delay()

        # cache default plot views & dataframe json
        result['avg_plot_result'] = plots.results[0]
        cache.add(cache_dict['plot1'], result['avg_plot_result'])

        # result['distance_plot_result'] = plots.results[1]
        # cache.add(cache_dict['plot2'], result['distance_plot_result'])

        result['distance_plot_3d_result'] = plots.results[1]
        cache.add(cache_dict['plot2'], result['distance_plot_3d_result'])

        result['df_json'] = plots.parent
        cache.add(cache_dict['df'], result['df_json'])

    else:
        # retrieve from cache
        result['df_json'] = cache.get(cache_dict['df'])
        result['avg_plot_result'] = cache.get(cache_dict['plot1'])
        # result['distance_plot_result'] = cache.get(cache_dict['plot2'])
        result['distance_plot_3d_result'] = cache.get(cache_dict['plot2'])

    return result

def getDistancePlotForm(year):
    dform = DistancePlotForm()

    # mindate = datetime(int(year), 1, 1)
    # maxdatetime = mindate + offsets.YearEnd()
    # maxdate = maxdatetime.date()
    #
    # dform.fields['day'].widget.config['options']['minDate'] = mindate.strftime('%Y/%m/%d')
    # dform.fields['day'].widget.config['options']['maxDate'] = maxdate.strftime('%Y/%m/%d')
    
    return dform

class index(View):
    index_template = 'index.html'

    def get(self, request, network_id, start_year=1975):
        data = get_data(network_id,start_year)

        ptm_ids = [p['id'] for p in data['ptm']]
        ptm_network = NetworkWithGeometry.objects.filter(id__in=ptm_ids)
        geojson = serialize('geojson', ptm_network,
                  geometry_field='point',
                  fields=('pk', 'id_to', 'dist2ocean'))

        # dform = getDistancePlotForm(start_year)

        context = {'network_id':network_id,'network_json': geojson, 'avg_plot_task_id': data['avg_plot_result'].task_id,
                   'distance_plot_3d_task_id': data['distance_plot_3d_result'].task_id, 'data_scope_form': DataScopeForm(),}

        return render(request, self.index_template, context)


def DataScopeView(request):
    if request.method == "POST" and request.is_ajax():
        network_id = request.POST['network_id']
        year = request.POST['year']
        data = get_data(network_id, int(year))

        return JsonResponse({"success": True,'year':year, 'avg_plot_task_id': data['avg_plot_result'].task_id,
                   'distance_plot_3d_task_id': data['distance_plot_3d_result'].task_id,}, status=200)
    return JsonResponse({"success": False}, status=400)


def DistancePlotView(request):
    if request.method == "POST" and request.is_ajax():
        network_id = request.POST['network_id']
        date = datetime.strptime(request.POST['day'],'%m/%d/%Y')
        year = date.year
        day_of_year = date.strftime('%j')

        cache_dict = get_cache_ids(network_id,year)
        df_json_task_id = cache.get(cache_dict['df'])

        data = distance_plot.delay(df_json_task_id.result, year, day_of_year)

        return JsonResponse({"success": True,'year':year,
                   'distance_plot_task_id': data.task_id}, status=200)
    return JsonResponse({"success": False}, status=400)


from django.http import HttpResponse
import pandas as pd

def download_csv(request,network_id=500,year=1975):

    #TODO: Handle case not in cache already
    cache_dict = get_cache_ids(network_id, year)
    df_json = cache.get(cache_dict['df']).result
    df = pd.read_json(df_json)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}_{}.csv'.format(network_id,year)

    df.to_csv(path_or_buf=response,sep=',',index=True,decimal=".")
    return response