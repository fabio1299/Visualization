from django.contrib.gis.db import models
from django.db import connection

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

    def get_catchment(self):
        with connection.cursor() as cursor:

            #This does not work
            cursor.execute("SELECT * FROM get_catchment(%s)", (self.id,))

            # This works
            cursor.execute("SELECT * FROM get_proj4_from_srid(%s)", (3857,))
            return cursor.fetchall()
