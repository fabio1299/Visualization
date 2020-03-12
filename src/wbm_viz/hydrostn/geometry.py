"""Django geometry operations"""

from django.contrib.gis.geos import GEOSGeometry, GeometryCollection


def get_geometrycollection(table_dict):
    """Return a GeometryCollection object from the table dictionary"""
    return GeometryCollection([GEOSGeometry(row['geom']) for row in table_dict])
