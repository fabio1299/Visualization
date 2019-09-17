from django.urls import path,re_path
from argentina import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gauges/', views.GaugeListView.as_view(), name='gauges-list'),
    re_path(r'^gauge/(?P<code>\d+)$', views.gauge_detail_view, name='gauge-detail'),
    re_path(r'^gauge/$', views.gauge_detail_view, name='gauge-detail'),
    re_path(r'^points.data/?(?P<b>\d+)?/?$', views.gauge_view, name='gauges'),
    re_path(r'^points.data/$', views.gauge_view, name='gauges'),
    re_path(r'^catchment.data/?(?P<b>\d+)?/?$', views.catchment_view, name='catchment'),
    re_path(r'^catchment.data/$', views.catchment_view, name='catchment'),
    re_path(r'^discharge/(?P<code>\d+)$', views.Graph.as_view(), name='gauge-discharge'),
    re_path(r'^discharge.data/(?P<code>\d+)$', views.export_data_xls, name='download-discharge'),
]