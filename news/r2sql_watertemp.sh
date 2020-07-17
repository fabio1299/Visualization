#!/bin/bash
raster2pgsql -p NETCDF:"qxt_watertemp_dTS1975.nc":QxT_WaterTemp -I -M -s 4326 -l 2,4 -N -9999.0 -t 50x50 -F  public.qxt_watertemp | psql -p 5435 -d news
for filename in /asrc/ecr/NEWS/Visualization/Scenarios/GFDL-ESM2M_RCP2p6_Final925/qxt_watertemp/*.nc; do
      raster2pgsql -a NETCDF:"$filename":QxT_WaterTemp -s 4326 -l 2,4 -N -9999.0 -t 50x50 -F public.qxt_watertemp | psql  -p 5435 -d news
done