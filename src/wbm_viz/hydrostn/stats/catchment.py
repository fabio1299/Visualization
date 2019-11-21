from django.db import connections
from django.contrib.gis.geos import GEOSGeometry,GeometryCollection


def dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_geometrycollection(table_dict):
    """Return a GeometryCollection object from the table dictionary"""
    return GeometryCollection([GEOSGeometry(row['geom']) for row in table_dict])


def get_catchment_table(subbasin):
    """Return table of subbasins forming catchment of a given Hydrostn30Subbasin object"""
    with connections['argentina_01min'].cursor() as cursor:
        cursor.callproc('get_catchment_table', (subbasin.id,))

        return dict_fetch_all(cursor)






