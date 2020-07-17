import xarray as xr
import subprocess as sp
import os
from sqlalchemy import create_engine
import pickle

# NOTE: Working with raster2pgsql this way turned out to be a a failed experiment really.
# However, maybe some of this code is of use/reference.

def run_subprocess(cmd, cwd):
    """Default config for running subprocess"""
    return sp.run(cmd, capture_output=True, shell=True, cwd=cwd).stdout.decode("utf-8")


def get_data(nc_filepath):
    """Get band date strings & model"""
    model = nc_filepath.split('/')[-3]
    with xr.open_dataset(nc_filepath) as ds:
        band_datetimes = [dt.__str__()[0:10] for dt in ds.time.data]
        return ds, model, band_datetimes


def file_dir(filepath):
    f = filepath.split('/')[-1]
    directory = os.path.dirname(filepath)
    return f, directory


def prep_raster_table(nc_filepath, table, schema='public'):
    nc_file, nc_dir = file_dir(nc_filepath)
    cmd = 'raster2pgsql -I -p -C -M NETCDF:"{}":AirTemperature -F -b 1 {}.{}'.format(nc_file, schema, table)
    sql = run_subprocess(cmd, nc_dir)
    default_columns = '"rid" serial PRIMARY KEY,"rast" raster,"filename" text'
    sql = sql.replace(default_columns, default_columns + ', "datetime" date, "model" text')
    return sql


def append_raster(nc_filepath, table, schema='public'):
    nc_file, nc_dir = file_dir(nc_filepath)
    __, model, datetimes = get_data(nc_filepath)

    sql_inserts = []
    for band, dt in enumerate(datetimes):
        cmd = 'raster2pgsql -a NETCDF:"{}":AirTemperature -F -b {} {}.{}'.format(nc_file, band+1, schema, table)
        sql = run_subprocess(cmd, nc_dir).split('\n')
        sql[1] = sql[1].replace('"rast","filename"', '"rast","filename","datetime","model"')
        sql[1] = sql[1][:-3] + "','{}','{}".format(dt, model) + sql[1][-3:]
        sql_inserts.append('\n'.join(sql))

    return sql_inserts


def stack_latlon(da):
    da = da.stack(lat_lon=['latitude','longitude'])
    return da


def apply_latlon(da_band, func, kwargs):
    """Apply func to each time,lat,lon,value in da which isn't NA/null
    
    da_band: band of dataarray of netcdf from NEWS/Visualization/*
    foo: function accepting datetime, lat double, lon double, val double
    """
    da_band = stack_latlon(da_band)
    result = []
    da_band = da_band[da_band.notnull()]
    kwargs['date'] = str(da_band.time.values)[0:10]
    for lat, lon in da_band.lat_lon.values:
        kwargs['lat'] = lat
        kwargs['lon'] = lon
        kwargs['val'] = da_band.sel({'lat_lon': (lat, lon)}).values.tolist()
        temp = func(**kwargs)
        result.append(temp)
    return result

def get_insert_tuple(model=None, date=None, lat=None, lon=None, val=None):
    return "('{}','{}','{}','{}','{}')".format(model, date, lat, lon, val)

def insert_chunks(values,table, engine=None, chunk_size=1000):
    template = """INSERT INTO {} (model, date, latitude, longitude, temperature) VALUES """.format(table)
    total = len(values)
    current = 0
    with engine.connect() as connection:
        while total > 0:
            values_chunk = values[current:current+chunk_size]
            sql = template + ','.join(values_chunk) + ';'
            total -= chunk_size
            current += chunk_size
            connection.execute(sql)


def nc2db(nc_filepath,uri):
    ds, model, band_datetimes = get_data(nc_filepath)
    engine = create_engine(uri)
    for band in ds.AirTemperature:
        inserts = apply_latlon(band, get_insert_tuple, {'model': model})

        pickle_dir = os.path.join('pickle', model, 'air_temperature')
        if not os.path.exists(pickle_dir):
            os.makedirs(pickle_dir)

        pickle.dump(inserts, open(os.path.join(pickle_dir, str(band.time.values)[0:10]+'.p'), 'wb'))
        insert_chunks(inserts, 'air_temperature_by_cell', engine=engine)
        print(str(band.time.values), 'completed')


if __name__ == '__main__':
    print('main')
    from news import get_netcdf_paths
    files = get_netcdf_paths()
    test_dir = files['NorESM1-M_RCP2p6_Final925']['airtemperature']
    for test_file in test_dir:
        nc2db(test_file)
        print(test_file, 'imported')

