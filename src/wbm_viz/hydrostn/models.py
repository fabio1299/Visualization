from django.contrib.gis.db import models
from django.db import connections
from django.contrib.gis.geos import GEOSGeometry

class Hydrostn30Subbasin(models.Model):
    id = models.IntegerField(primary_key=True)
    record_name = models.CharField(max_length=12, blank=True, null=True)
    grid_value = models.IntegerField(blank=True, null=True)
    grid_area = models.FloatField(blank=True, null=True)
    grid_percent = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    vertex_num = models.IntegerField(blank=True, null=True)
    basin_id = models.IntegerField(blank=True, null=True)
    stream_order = models.IntegerField(blank=True, null=True)
    from_x_coord = models.FloatField(blank=True, null=True)
    from_y_coord = models.FloatField(blank=True, null=True)
    to_x_coord = models.FloatField(blank=True, null=True)
    to_y_coord = models.FloatField(blank=True, null=True)
    cell_id = models.IntegerField(blank=True, null=True)
    basin_name = models.CharField(max_length=32, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    number_of_cells = models.IntegerField(blank=True, null=True)
    stn_mainstem_length = models.FloatField(blank=True, null=True)
    stn_catchment_area = models.FloatField(blank=True, null=True)
    stn_interstation_area = models.FloatField(blank=True, null=True)
    next_station = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'hydrostn30_subbasin'
        app_label = 'hydrostn'

    @property
    def get_catchment(self):
        """Return upstream catchment as geojson"""
        with connections['argentina_01min'].cursor() as cursor:

            cursor.callproc('get_catchment', (self.id,))

            # return from db is in hexadecimal representation
            hex_wkb = cursor.fetchone()[0]

            # convert to polygon
            polygon = GEOSGeometry(hex_wkb)
            return polygon.geojson

class CatchmentBasins(models.Model):
    sample_id = models.IntegerField(primary_key=True)
    basins = models.TextField(blank=True, null=True)  # This field type is a guess.
    catchment = models.GeometryField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_basins'
        app_label = 'hydrostn'


class CatchmentStatsAirTemperature(models.Model):
    subbasin_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    mean_zonal_mean = models.FloatField(blank=True, null=True)
    mean_zonal_min = models.FloatField(blank=True, null=True)
    mean_zonal_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_stats_air_temperature'
        app_label = 'hydrostn'


class CatchmentStatsEvapotranspiration(models.Model):
    subbasin_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    mean_zonal_mean = models.FloatField(blank=True, null=True)
    mean_zonal_min = models.FloatField(blank=True, null=True)
    mean_zonal_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_stats_evapotranspiration'
        app_label = 'hydrostn'


class CatchmentStatsPrecipitation(models.Model):
    subbasin_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    mean_zonal_mean = models.FloatField(blank=True, null=True)
    mean_zonal_min = models.FloatField(blank=True, null=True)
    mean_zonal_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_stats_precipitation'
        app_label = 'hydrostn'


class CatchmentStatsRunoff(models.Model):
    subbasin_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    mean_zonal_mean = models.FloatField(blank=True, null=True)
    mean_zonal_min = models.FloatField(blank=True, null=True)
    mean_zonal_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_stats_runoff'
        app_label = 'hydrostn'

class CatchmentStatsSoilMoisture(models.Model):
    subbasin_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    mean_zonal_mean = models.FloatField(blank=True, null=True)
    mean_zonal_min = models.FloatField(blank=True, null=True)
    mean_zonal_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catchment_stats_soil_moisture'
        app_label = 'hydrostn'




