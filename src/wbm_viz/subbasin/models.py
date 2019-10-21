from django.contrib.gis.db import models

# Create your models here.
class Subbasin(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    recordname = models.CharField(db_column='RecordName', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gridvalue = models.IntegerField(db_column='GridValue', blank=True, null=True)  # Field name made lowercase.
    gridarea = models.FloatField(db_column='GridArea', blank=True, null=True)  # Field name made lowercase.
    gridpercent = models.FloatField(db_column='GridPercent', blank=True, null=True)  # Field name made lowercase.
    perimeter = models.FloatField(db_column='Perimeter', blank=True, null=True)  # Field name made lowercase.
    vertexnum = models.IntegerField(db_column='VertexNum', blank=True, null=True)  # Field name made lowercase.
    basinid = models.IntegerField(db_column='BasinID', blank=True, null=True)  # Field name made lowercase.
    streamorder = models.IntegerField(db_column='StreamOrder', blank=True, null=True)  # Field name made lowercase.
    fromxcoord = models.FloatField(db_column='FromXCoord', blank=True, null=True)  # Field name made lowercase.
    fromycoord = models.FloatField(db_column='FromYCoord', blank=True, null=True)  # Field name made lowercase.
    toxcoord = models.FloatField(db_column='ToXCoord', blank=True, null=True)  # Field name made lowercase.
    toycoord = models.FloatField(db_column='ToYCoord', blank=True, null=True)  # Field name made lowercase.
    cellid = models.IntegerField(db_column='CellID', blank=True, null=True)  # Field name made lowercase.
    basinname = models.CharField(db_column='BasinName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    color = models.IntegerField(db_column='Color', blank=True, null=True)  # Field name made lowercase.
    numberofcells = models.IntegerField(db_column='NumberOfCells', blank=True, null=True)  # Field name made lowercase.
    stnmainstemlength = models.FloatField(db_column='STNMainstemLength', blank=True, null=True)  # Field name made lowercase.
    stncatchmentarea = models.FloatField(db_column='STNCatchmentArea', blank=True, null=True)  # Field name made lowercase.
    stninterstationarea = models.FloatField(db_column='STNInterStationArea', blank=True, null=True)  # Field name made lowercase.
    nextstation = models.IntegerField(db_column='NextStation', blank=True, null=True)  # Field name made lowercase.# This is an auto-generated Django model module.
    geom = models.PolygonField(db_column="geom",blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'Subbasin'
        app_label = 'subbasin'
