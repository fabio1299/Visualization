--
-- CREATE TABLE catchment_stats_evapotranspiration(
--             subbasin_id integer,
--             date varchar(10),
--             model_name text,
--             mean_zonal_mean double precision,
--             mean_zonal_min double precision,
--             mean_zonal_max double precision
-- );
--
-- do $$
-- begin
-- for r in 1001..48077 loop
-- insert into catchment_stats_evapotranspiration SELECT * FROM catchment_evapotranspiration(r);
-- end loop;
-- end;
-- $$;
--
-- SELECT * FROM catchment_stats_evapotranspiration WHERE model_name = 'WBMprist_CRUTSv401' AND subbasin_id = 1;



CREATE TABLE catchment_stats_soil_moisture(
            subbasin_id integer,
            date varchar(10),
            model_name text,
            mean_zonal_mean double precision,
            mean_zonal_min double precision,
            mean_zonal_max double precision
);

do $$
begin
for r in 1..48077 loop
insert into catchment_stats_soil_moisture SELECT * FROM catchment_soil_moisture(r);
end loop;
end;
$$;