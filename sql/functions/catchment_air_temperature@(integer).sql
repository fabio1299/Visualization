create function catchment_air_temperature(integer)
    returns TABLE(subbasin_id integer, date character varying, model_name text, mean_zonal_mean double precision, mean_zonal_min double precision, mean_zonal_max double precision)
    language plpgsql
as
$$
    #variable_conflict use_column
    DECLARE
        subbasin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT subbasin_id,
                             date,
                             "model_name",
--                           Weighted Average by Subbasin Area
                             SUM(zonal_mean * zone_area)/SUM(zone_area) as mean_zonal_mean,
                             SUM(zonal_min * zone_area)/SUM(zone_area) as mean_zonal_min,
                             SUM(zonal_max * zone_area)/SUM(zone_area) as mean_zonal_max
         FROM subbasin_air_temperature_monthly
         WHERE subbasin_id in (SELECT id FROM get_catchment_table(subbasin_id))
         GROUP BY "date", "model_name"
         ORDER BY date;
END;
$$;
