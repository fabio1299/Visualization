from django.contrib import admin

# Register your models here.
from django.contrib.gis import admin
from .models import *

class GaugeAdmin(admin.OSMGeoAdmin):
    list_display = ('code', 'station_name', 'province', 'river_name')
    list_filter = ['river_name']

# Register the admin class with the associated model
#admin.site.register(Gauge01Min, GaugeAdmin)
admin.site.register(GaugeDischarge01Min, admin.OSMGeoAdmin)
