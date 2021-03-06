"""wbm_viz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from django.views.generic.base import RedirectView
from hydrostn import views


urlpatterns = [
    path('', RedirectView.as_view(url='/argentina/1')),
    path('argentina/', RedirectView.as_view(url='/argentina/1')),
    path('peru/', RedirectView.as_view(url='/peru/1')),
    re_path(r'^(?P<country>argentina|peru)/(?P<subbasin_id>\d+)/$', views.HomeView.as_view(), name='home'),
    re_path(r'^(?P<country>argentina|peru)/(?P<lat>-?\d+.\d+)/(?P<lon>-?\d+.\d+)/$', views.StationRedirect, name='station_redirect')
]
