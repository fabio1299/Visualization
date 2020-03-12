"""Database calls which circumvent the model abstraction"""
from django.db import connections
from django.contrib.gis.geos import Point

def _dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_catchment_table(subbasin,country,res):
    """Return table of subbasins forming catchment of a given Hydrostn30Subbasin object"""
    db = '{}_{}'.format(country,res)
    with connections[db].cursor() as cursor:
        cursor.callproc('get_catchment_table', (subbasin.id,))

        return _dict_fetch_all(cursor)

def get_container_geometry(lon, lat, model, field='geom'):
    """Return the model instance with geometry that contains a given point

    Ex: get_container_geometry(-62.897611,-27.72973,ArgentinaHydrostn30Subbasin,'geom')
    """
    p = Point(lon, lat)
    kwargs = {'{}__contains'.format(field): p, }
    return model.objects.filter(**kwargs)
