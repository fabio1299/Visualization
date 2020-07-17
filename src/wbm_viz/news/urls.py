from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from news import views


urlpatterns = [
    # path('', views.index.as_view())
    path('', RedirectView.as_view(url='/news/1')),
    re_path(r'^(?P<network_id>\d+)/$', views.index.as_view(), name='news'),
    re_path(r'^(?P<network_id>\d+)/(?P<year>\d+)/download/$', views.download_csv, name='download_csv'),
    # path('download/',views.download_csv,name='download'),
    # ajax
    path('ajax/data-scope/', views.DataScopeView, name='data-scope-update'),
    path('ajax/distance-plot/', views.DistancePlotView, name='distance-plot-update'),
]


