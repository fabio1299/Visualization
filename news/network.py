from news.network_functions import *
from news.news import to_db

def wkb_hexer(line):
    return line.wkb_hex

if __name__ == '__main__':
    network = '/asrc/ecr/NEWS/Visualization/Network/NetworkWithDistance.txt'
    df = LoadDBCells(network)
    addToNodeID(df)
    CRS = "EPSG:4326"
    gdf1 = makeGDF_points(df, CRS)
    gdf1.rename(columns={'geometry': 'point'}, inplace=True)
    gdf1['point'] = gdf1['point'].apply(wkb_hexer)

    gdf2 = makeGDF_lines(df, CRS)
    gdf2.rename(columns={'geometry': 'line'}, inplace=True)
    gdf2['line'] = gdf2['line'].apply(wkb_hexer)

    gdf1['line'] = gdf2['line']
    print('Geodataframe prepped')

    geom_sql = """
    CREATE INDEX ON network ("GeoID");
    CREATE INDEX ON network ("ID");
    ALTER TABLE network_with_geometry
    ALTER COLUMN point TYPE Geometry(POINT, 4326)
                     USING ST_SetSRID(point::Geometry, 4326);
    ALTER TABLE network_with_geometry
    ALTER COLUMN line TYPE Geometry(LINESTRING, 4326)
                     USING ST_SetSRID(line::Geometry, 4326);
    """
    geom_postsql = [geom_sql, ]

    print('Attempting write to DB')
    to_db(gdf1, 'network_with_geometry', geom_postsql)