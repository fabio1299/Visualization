"""Django wrappers for database stored procedures"""
from django.db import connections


def _dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_catchment_table(subbasin):
    """Return table of subbasins forming catchment of a given Hydrostn30Subbasin object"""

    with connections['argentina_01min'].cursor() as cursor:
        cursor.callproc('get_catchment_table', (subbasin.id,))

        return _dict_fetch_all(cursor)