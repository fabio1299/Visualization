from django.db import connections

def get_catchment_table(subbasin):
    with connections['argentina_01min'].cursor() as cursor:
        cursor.callproc('get_catchment_table', (subbasin.id,))

        return cursor.fetchall()

        # # return from db is in hexadecimal representation
        # hex_wkb = cursor.fetchone()[0]
        #
        # # convert to polygon
        # polygon = GEOSGeometry(hex_wkb)
        # return polygon.geojson