from django.views import generic
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.serializers import serialize
from rest_framework import serializers
import sys
import pandas as pd

# import xlsxwriter

if sys.version_info[0] < 3:
    from io import StringIO as IO  # python 2
else:
    from io import BytesIO as IO  # for python 3+

from django_pandas.io import read_frame
import plotly.offline as opy
import plotly.graph_objs as go
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import argentina.plots_plotly as pp
import argentina.plots_bokeh as pb

from .models import *

filter = [16, 693, 811, 1211, 1219, 1403, 1413, 1423, 1424, 1451,
          1452, 1453, 1605, 1801, 1808, 1809, 2002, 2096, 2207,
          2295, 2297, 2401, 2602, 2606, 2824, 3216, 3223, 3401,
          3442, 3448, 3802, 3805, 3862]

# filter = None

library = 'plotly'  # alternative values are 'bokeh' or 'plotly'


# Create your views here.
# class GaugesSerializer(serializers.ModelSerializer):

#    get_absolute_url = serializers.SerializerMethodField() # define a SerializerMethodField

#    def get_absolute_url(self, obj):
#        return obj.get_absolute_url() # return the absolute url of the object

#    class Meta:
#        model = Gauge01MinGeoj
#        fields = ('id', 'code', 'province', 'river_name', 'station_name', 'catchment_area',
#                  'point', 'catchment', 'get_absolute_url')


class GaugeListView(generic.ListView):
    allow_empty = False
    model = Gauge01MinMinimal
    context_object_name = 'gauge_list'
    template_name = 'argentina/gauge_list.html'

    def get_queryset(self, *args, **kwargs):
        if filter is None:
            return Gauge01MinMinimal.objects.all()
        else:
            return Gauge01MinMinimal.objects.filter(code__in=filter)


# class GaugeDetailView(generic.DetailView):
#    model = Gauge01Min
#    context_object_name = 'gauge'
#    template_name = 'argentina/gauge_detail.html'
##    def get_queryset(self, *args, **kwargs):
##        return Gauge01MinMinimal.objects.all()

def gauge_detail_view(request, code=None):
    # code=request.GET.get('selectcode')
    # print(code)
    gauge = get_object_or_404(Gauge01MinGeoj, code=code)
    # gauge.catchment_area='{:,.2f}'.format(gauge.catchment_area)
    gauge.catchment_area = '{:,.0f}'.format(gauge.catchment_area)
    return render(request, 'argentina/gauge_detail.html', context={'gauge': gauge})


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects

    graph_list = []

    if filter is None:
        num_stations = Gauge01MinMinimal.objects.all().count()
        num_rivers = Gauge01MinMinimal.objects.values('river_name').distinct().count()
        num_provinces = Gauge01MinMinimal.objects.values('province').distinct().count()
    else:
        num_stations = Gauge01MinMinimal.objects.filter(code__in=filter).count()
        num_rivers = Gauge01MinMinimal.objects.filter(code__in=filter).values('river_name').distinct().count()
        num_provinces = Gauge01MinMinimal.objects.filter(code__in=filter).values('province').distinct().count()
        graph_list.append(
            pp.ModPerformance(GaugeDischarge01Min.objects.filter(code__in=filter).to_timeseries(index='mydate')))

    # stations=GaugeListView

    context = {
        'num_stations': num_stations,
        'num_rivers': num_rivers,
        'num_provinces': num_provinces,
        'home_page': "active",
        'perf_tab': graph_list
    }
    return render(request, 'index.html', context)


def catchment_view(request, b=None):
    if b is None:
        # founds =  Gauge01MinGeoj.objects.all()
        # catchment_as_geojson = serialize('geojson', founds , fields=('code','catchment',))
        return
    else:
        founds = Gauge01MinGeoj.objects.filter(code=b)
        catchment_as_geojson = serialize('geojson', founds, fields=('code', 'catchment',))
        catchment_as_geojson = catchment_as_geojson.replace('"}, "geometry": null', '')
        catchment_as_geojson = catchment_as_geojson.replace(', "catchment": "', '}, "geometry":')
        catchment_as_geojson = catchment_as_geojson.replace('\\"type\\":\\"Polygon\\",\\"coordinates\\"',
                                                            '"type":"Polygon","coordinates"')
    return HttpResponse(catchment_as_geojson, content_type='json')


# def catchment_view(request,b=None):
#    if b is None:
#        founds =  Gauge01MinGeoj.objects.values('catchment').all()
#        #catchment_as_geojson = serialize('geojson', founds , fields=('code','catchment',))
#    else:
#        founds =  Gauge01MinGeoj.objects.filter(code=b)
#        catchment_as_geojson = serialize('geojson', founds , fields=('code','catchment',))
#        #catchment_as_geojson.replace(', "geometry": null','')
#        #catchment_as_geojson.replace('"catchment"','"geometry"')
#    return HttpResponse(catchment_as_geojson.replace(', "geometry": null','').replace('"catchment"','"geometry"'), content_type='json')

def gauge_view(request, b=None):
    if b is None:
        if filter is None:
            founds = Gauge01MinGeoj.objects.all()
            # serialized=GaugesSerializer(founds,many=True)
            points_as_geojson = serialize('geojson', founds)  # , fields=('code','point'))
        else:
            founds = Gauge01MinGeoj.objects.filter(code__in=filter)
            # serialized=GaugesSerializer(founds,many=True)
            points_as_geojson = serialize('geojson', founds)  # , fields=('code','point'))
    else:
        founds = Gauge01MinGeoj.objects.all().filter(code=b)
        points_as_geojson = serialize('geojson', founds, fields=('code', 'point'))
    return HttpResponse(points_as_geojson, content_type='json')


class Graph(generic.TemplateView):
    template_name = 'argentina/gauge_graph.html'

    def get_context_data(self, **kwargs):

        dfDischarge = (GaugeDischarge01Min.objects.filter(code=kwargs['code'])).to_timeseries(index='mydate')

        station_info = Gauge01MinMinimal.objects.filter(code=kwargs['code'])

        context = super(Graph, self).get_context_data(**kwargs)
        context['station'] = station_info[0]
        context['library'] = library

        graph_list = []

        if library == 'plotly':
            graph_list.append(pp.TimeseriesAllModels(dfDischarge, kwargs['code'], 'Pippo'))
            graph_list.append(pp.TimeseriesAnnualAllModels(dfDischarge, kwargs['code'], 'Pippo'))
            graph_list.append(pp.BoxplotMonthlyAllModels(dfDischarge, kwargs['code'], 'Pippo'))
            # graph_list.append(pp.StasTable(dfDischarge,kwargs['code'],'Pippo'))
            graph_list.append(pp.ObsVsModeled(dfDischarge, 'terraclimate_ro', kwargs['code'], 'Pippo'))
            graph_list.append(pp.ObsVsModeled(dfDischarge, 'terraclimate_wbm', kwargs['code'], 'Pippo'))
            graph_list.append(pp.ObsVsModeled(dfDischarge, 'crutsv401', kwargs['code'], 'Pippo'))
            graph_list.append(pp.ObsVsModeled(dfDischarge, 'gpccv7', kwargs['code'], 'Pippo'))
            context['graphs'] = graph_list
            return context

        elif library == 'bokeh':
            graph_list.append(pb.ObsVsModeled(dfDischarge, 'terraclimate_ro', kwargs['code'], 'Pippo'))
            graph_list.append(pb.ObsVsModeled(dfDischarge, 'terraclimate_wbm', kwargs['code'], 'Pippo'))
            context['graphs'] = graph_list
            return context
            # print(graph.keys())
            # return render_to_response( 'argentina/bokeh.html', graph)
        else:
            print('unknown graphic library')
            return


def export_data_xls(request, code=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    dfDischarge = GaugeDischarge01Min.objects.filter(code=code).to_timeseries(index='mydate')
    station_info = Gauge01MinMinimal.objects.filter(code=code)

    # my "Excel" file, which is an in-memory output file (buffer)
    # for the new workbook
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    dfDischarge.to_excel(xlwriter, station_info.values()[0]['station_name'])

    xlwriter.save()
    xlwriter.close()

    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=DischargeStation{}.xlsx'.format(code)

    print(response)

    return response
