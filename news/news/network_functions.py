import pandas as pd
import geopandas as gp
import shapely.geometry as geom
import subprocess as sp
from io import StringIO
import os

# Dictionary used to convert flow direction into
# coordinates offset
coordFilter = {1: [1, 0],
               2: [1, -1],
               4: [0, -1],
               8: [-1, -1],
               16: [-1, 0],
               32: [-1, 1],
               64: [0, 1],
               128: [1, 1]}
# Resolution of the Network being analysed
Resolution = 0.05
# Names of columns in dataset
ToCell = "ToCell"
Latitude = "CellYCoord"
Longitude = "CellXCoord"


####################################################

def LoadDBCells(inFile):
    # Loads a network DBCells table from inFile into a Pandas DataFrame
    # Can load both an RGIS gdbn file and a CSV
    print('Loading network from file {}'.format(inFile))
    filename, file_extension = os.path.splitext(inFile)
    if file_extension == '.gdbn':
        cmd = Dir2Ghaas + '/bin/rgis2table -a DBCells '
        proc = sp.Popen(cmd + inFile, stdout=sp.PIPE, shell=True)

        data1 = StringIO(bytearray(proc.stdout.read()).decode("utf-8"))
        data = pd.read_csv(data1, sep='\t')
    else:
        data = pd.read_csv(inFile, sep='\t')

    return data


#####################################################

def getCoordStr(Coord):
    # Returns the string-transformed coordinate trimmed to
    # 3 decimal points
    CoordStr = '{:8.3f}'.format(Coord)
    return CoordStr.strip()


def getCoordID(Lon, Lat):
    # Creates a unique ID based on the concatenating the
    # string representation of the cell's coordinates (GeoID)
    return getCoordStr(Lon) + '_' + getCoordStr(Lat)


def loadCoordID(row):
    # Use with:
    #         df["new column"] = df.apply(loadCoordID,axis=1)
    # construct to assign to a new column the unique GeoID
    # SEE: getCoordID...
    return getCoordID(row[Longitude], row[Latitude])


def nextCell(row):
    # Returns the x, y coordinates of the next cell in the network
    # Use wit the same construct used for the loadCoordID function...
    res = Resolution
    tocellv = row[ToCell]
    lon = row[Longitude]
    lat = row[Latitude]
    return findNext(tocellv, lon, lat, res)


def findNext(tocell, lon, lat, res):
    # Returns the GeoID of the next cell in the network
    # Uses the CoordFilter dictionary to convert the
    # flow direction into coordinate offset
    if tocell == 0:
        # we have a sink, nothing to do
        return ''
    else:
        x = lon + coordFilter[tocell][0] * res
        y = lat + coordFilter[tocell][1] * res
    return getCoordID(x, y)


def returnCoordArrays(geo_id):
    # Returns the Latitude and Longitude (in Decimal Degrees) from the GeoID
    lon = [float(x.split('_')[0]) for x in geo_id]
    lat = [float(x.split('_')[1]) for x in geo_id]
    return lon, lat


def addToNodeID(dfNet):
    # Adds the "GeoID", "GeoID_To" and the "ID_To" columns to the Network's dataframe
    print('Adding ToNode ID to Network DataFrame')
    dfNet['GeoID'] = dfNet.apply(loadCoordID, axis=1)
    dfNet['GeoID_To'] = dfNet.apply(nextCell, axis=1)
    dfIDs = dfNet[['GeoID', 'ID']]
    dfIDs.set_index('GeoID', drop=False, inplace=True)
    dfNet.set_index('GeoID_To', drop=False, inplace=True)
    dfNet['ID_To'] = dfIDs['ID']
    dfNet.loc[dfNet['ID_To'].isnull(), 'ID_To'] = 0
    dfNet['ID_To'] = dfNet['ID_To'].astype('int')
    dfNet['Split'] = 1.0
    dfNet.reset_index(drop=True, inplace=True)
    return dfIDs


def pointGeometry(lon, lat):
    # Creates a Point geometry object from lat lon coordinates
    # Requires shapely and geopandas packages
    Points = [geom.Point(xy) for xy in zip(lon, lat)]
    return Points


def lineGeometry(dfNet):
    # Creates a list of all the Line geometry objects for the entire
    # network
    #
    # Requires shapely and geopandas packages
    #
    # Where we have no GeoID_To, we set it same as GeoID
    # e.g. will result in a zero-length line
    dfNet.loc[dfNet['GeoID_To'] == '', 'GeoID_To'] = dfNet['GeoID']

    from_lon, from_lat = returnCoordArrays(dfNet['GeoID'].values)
    FromNodes = pointGeometry(from_lon, from_lat)

    to_lon, to_lat = returnCoordArrays(dfNet['GeoID_To'].values)
    ToNodes = pointGeometry(to_lon, to_lat)
    Lines = [geom.LineString(ar) for ar in zip(FromNodes, ToNodes)]
    return Lines


def makeGDF_lines(dfNet, crs):
    # Adds the line geometry to the Network's dataframe
    # Note the crs is a Coordinate Reference System object
    #
    # Requires shapely and geopandas packages

    print('Adding Line geometry to GeoPandas DataFrame')
    Lines = lineGeometry(dfNet)
    gdNet = gp.GeoDataFrame(dfNet, crs=crs, geometry=Lines)
    cols = ['ID', 'Name', 'ToCell', 'FromCell', 'Order', 'BasinID', 'BasinCells',
            'Travel', 'CellArea', 'CellLength', 'SubbasArea', 'SubbaLengh',
            'CellXCoord', 'CellYCoord', 'Dist2Mouth', 'Dist2Ocean', 'GeoID',
            'GeoID_To', 'ID_To', 'Split', 'geometry']
    gdNet.columns = cols
    gdNet.drop(labels=['GeoID',
                       'GeoID_To', 'Split'], axis=1, inplace=True)
    return gdNet


def makeGDF_points(dfNet, crs):
    # Adds the point geometry to the Network's dataframe
    # Note the crs is a Coordinate Reference System object
    #
    # Requires shapely and geopandas packages

    print('Adding Point geometry to GeoPandas DataFrame')
    lon, lat = returnCoordArrays(dfNet['GeoID'].values)
    Points = pointGeometry(lon, lat)
    gdNet = gp.GeoDataFrame(dfNet, crs=crs, geometry=Points)
    cols = ['ID', 'Name', 'ToCell', 'FromCell', 'Order', 'BasinID', 'BasinCells',
            'Travel', 'CellArea', 'CellLength', 'SubbasArea', 'SubbaLengh',
            'CellXCoord', 'CellYCoord', 'Dist2Mouth', 'Dist2Ocean', 'GeoID',
            'GeoID_To', 'ID_To', 'Split', 'geometry']
    gdNet.columns = cols
    gdNet.drop(labels=['GeoID',
                       'GeoID_To', 'Split'], axis=1, inplace=True)
    return gdNet
