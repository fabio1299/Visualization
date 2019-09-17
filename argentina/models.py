from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse

from django_pandas.managers import DataFrameManager

class SelectedStationsManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(models.Manager, self).__init__(*args, **kwargs)
        self.filterby = None

    def get_queryset(self):
        if self.filterby is None:
            return super(SelectedStationsManager, self).get_queryset()
        else:
            return super(SelectedStationsManager, self).get_queryset().filter(sex=self.filterby)

# Create your models here.
class Gauge01MinMinimal(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    code = models.BigIntegerField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    river_name = models.TextField(blank=True, null=True)
    station_name = models.TextField(blank=True, null=True)
    catchment_area = models.FloatField(blank=True,null=True)
#    place= models.GeometryField(blank=True, null=True)
    place= models.GeometryField(blank=True, db_column='point', null=True)

    #def __init__(self, *args, **kwargs):
    #    super(models.Model, self).__init__(*args, **kwargs)
    #    self.filterby = None

    class Meta:
        managed = False  # Created from a view. Don't remove.
#        db_table = 'get_gauge_01min_minimal'
        db_table = 'get_gauge_01min_geoj_new'
        app_label = 'argentina'

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('gauge-detail', args=[str(self.code)])

    def get_download_url(self):
        """Returns the url to download data as excel file."""
        return reverse('download-discharge', args=[str(self.code)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.station_name

    #Manager=SelectedStationsManager

    #Manager.filterby=filterby

    #objects = Manager


#class Gauge01Min(models.Model):
#    id = models.BigIntegerField(blank=True, primary_key=True)
#    code = models.BigIntegerField(blank=True, null=True)
#    province = models.TextField(blank=True, null=True)
#    river_name = models.TextField(blank=True, null=True)
#    station_name = models.TextField(blank=True, null=True)
#    point = models.GeometryField(blank=True, null=True)
#    catchment = models.PolygonField(blank=True, null=True)

#    class Meta:
#        managed = False  # Created from a view. Don't remove.
#        db_table = 'get_gauge_01min'
#        app_label = 'argentina'

    # Methods
#    def get_absolute_url(self):
#        """Returns the url to access a particular instance of MyModelName."""
#        return reverse('gauge-discharge', args=[str(self.code)])

#    def __str__(self):
#        """String for representing the MyModelName object (in Admin site etc.)."""
#        return self.station_name


class Gauge01MinGeoj(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    code = models.BigIntegerField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    river_name = models.TextField(blank=True, null=True)
    station_name = models.TextField(blank=True, null=True)
    catchment_area = models.FloatField(blank=True,null=True)
    point = models.GeometryField(blank=True, null=True)
    catchment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        #db_table = 'get_gauge_01min_geoj'
        db_table = 'get_gauge_01min_geoj_new'
        app_label = 'argentina'

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('gauge-discharge', args=[str(self.code)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.station_name


class GaugeDischarge01Min(models.Model):
    #dbid = models.BigIntegerField(blank=True, null=True)
    code = models.BigIntegerField(blank=True, null=True)
    mydate = models.DateField(blank=True, null=True)
    obs = models.FloatField(blank=True, null=True)
    crutsv401 = models.FloatField(blank=True, null=True) # data source URL https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.01/
    gpccv7 = models.FloatField(blank=True, null=True) # data source URL https://www.dwd.de/EN/ourservices/gpcc/gpcc.html
    terraclimate_wbm = models.FloatField(blank=True, null=True)
    terraclimate_ro = models.FloatField(blank=True, null=True)

    objects = DataFrameManager()

    class Meta:
        managed = False  # Created from a view. Don't remove.
        #db_table = 'get_gauge_discharge_01min'
        db_table = 'get_gauge_discharge_01min_new'
        app_label = 'argentina'


