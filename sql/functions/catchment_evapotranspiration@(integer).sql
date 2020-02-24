create or replace function catchment_evapotranspiration(integer)
    returns TABLE(sample_id integer, date character varying, model_name text, mean_zonal_mean double precision, mean_zonal_min double precision, mean_zonal_max double precision)
    language plpgsql
as
$$
    #variable_conflict use_column
    DECLARE
        basin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT basin_id as sample_id,
                             date,
                             model_name,
--                           Weighted Average by Subbasin Area
                             SUM(zonal_mean * zone_area)/SUM(zone_area) as mean_zonal_mean,
                             SUM(zonal_min * zone_area)/SUM(zone_area) as mean_zonal_min,
                             SUM(zonal_max * zone_area)/SUM(zone_area) as mean_zonal_max
         FROM subbasin_evapotranspiration_monthly
         WHERE subbasin_id in (SELECT unnest(basins) from catchment_basins where sample_id = $1)
         GROUP BY date, model_name
         ORDER BY date;
END
$$;


