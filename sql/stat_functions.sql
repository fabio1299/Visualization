DROP FUNCTION catchment_air_temperature(integer);
CREATE OR REPLACE FUNCTION catchment_air_temperature(integer)
    RETURNS TABLE(
                    date varchar(10),
                    model_name text,
                    mean_zonal_mean double precision,
                    mean_zonal_min double precision,
                    mean_zonal_max double precision
                 )
AS $$
    #variable_conflict use_column
    DECLARE
        subbasin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT "Date",
                             "model_name",
--                           Weighted Average by Subbasin Area
                             SUM("ZonalMean" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_mean,
                             SUM("ZonalMin" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_min,
                             SUM("ZonalMax" * "ZoneArea")/SUM("ZoneArea") as mean_zonal_max
         FROM air_temperature_subbasin_monthly
         WHERE "SampleID" in (SELECT id FROM get_catchment_table(subbasin_id))
         GROUP BY "Date" ,"model_name"
         ORDER BY "Date";
END; $$
LANGUAGE PLPGSQL;

SELECT * FROM catchment_air_temperature(1000);

--
DROP FUNCTION catchment_evapotranspiration(integer);
CREATE OR REPLACE FUNCTION catchment_evapotranspiration(integer)
    RETURNS TABLE(
                    subbasin_id integer,
                    date varchar(10),
                    model_name text,
                    mean_zonal_mean double precision,
                    mean_zonal_min double precision,
                    mean_zonal_max double precision
                 )
AS $$
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
         FROM evapotranspiration_subbasin_monthly
         WHERE "SampleID" in (SELECT id FROM get_catchment_table(subbasin_id))
         GROUP BY "Date" ,"model_name"
         ORDER BY "Date";
END; $$
LANGUAGE PLPGSQL;

SELECT * FROM catchment_evapotranspiration(1000);


--

