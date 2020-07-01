from django.contrib.gis.db import models
from django.db import connections


class NetworkWithGeometry(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    tocell = models.BigIntegerField(db_column='ToCell', blank=True, null=True)  # Field name made lowercase.
    fromcell = models.FloatField(db_column='FromCell', blank=True, null=True)  # Field name made lowercase.
    order = models.BigIntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    basinid = models.BigIntegerField(db_column='BasinID', blank=True, null=True)  # Field name made lowercase.
    basincells = models.BigIntegerField(db_column='BasinCells', blank=True, null=True)  # Field name made lowercase.
    travel = models.BigIntegerField(db_column='Travel', blank=True, null=True)  # Field name made lowercase.
    cellarea = models.FloatField(db_column='CellArea', blank=True, null=True)  # Field name made lowercase.
    celllength = models.FloatField(db_column='CellLength', blank=True, null=True)  # Field name made lowercase.
    subbasarea = models.FloatField(db_column='SubbasArea', blank=True, null=True)  # Field name made lowercase.
    subbalengh = models.FloatField(db_column='SubbaLengh', blank=True, null=True)  # Field name made lowercase.
    cellxcoord = models.FloatField(db_column='CellXCoord', blank=True, null=True)  # Field name made lowercase.
    cellycoord = models.FloatField(db_column='CellYCoord', blank=True, null=True)  # Field name made lowercase.
    dist2mouth = models.FloatField(db_column='Dist2Mouth', blank=True, null=True)  # Field name made lowercase.
    dist2ocean = models.FloatField(db_column='Dist2Ocean', blank=True, null=True)  # Field name made lowercase.
    id_to = models.BigIntegerField(db_column='ID_To', blank=True, null=True)  # Field name made lowercase.
    point = models.PointField(blank=True, null=True)
    line = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'network_with_geometry'

    def path_to_mouth(self):
        """Return upstream catchment as geojson"""
        with connections['news'].cursor() as cursor:
            cursor.callproc('news_path_to_mouth', (self.id,))

            columns = [col[0].lower() for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]


class O2QxtWatertemp(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'o_2_qxt_watertemp'


class O4QxtWatertemp(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'o_4_qxt_watertemp'


class QxtWatertemp(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qxt_watertemp'
