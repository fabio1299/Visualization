create function catchment_runoff(integer)
    returns TABLE(subbasin_id integer, date character varying, model_name text, mean_zonal_mean double precision, mean_zonal_min double precision, mean_zonal_max double precision)
    language plpgsql
as
$$
    #variable_conflict use_column
    DECLARE
        subbasin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT subbasin_id as subbasin_id,
                             "Date",
                             "model_name",
--                           Weighted Average by Subbasin Area
                             SUM("ZonalMean" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_mean,
                             SUM("ZonalMin" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_min,
                             SUM("ZonalMax" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_max
         FROM runoff_subbasin_monthly
         WHERE "SampleID" in (SELECT id FROM get_catchment_table(subbasin_id))
         GROUP BY "Date" ,"model_name"
         ORDER BY "Date";
END;
$$;

alter function catchment_runoff(integer) owner to danielv;

