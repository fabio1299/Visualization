CREATE TABLE catchment_stats_air_temperature(
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
insert into catchment_stats_air_temperature SELECT * FROM catchment_air_temperature(r);
end loop;
end;
$$;

--

CREATE TABLE catchment_stats_precipitation(
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
insert into catchment_stats_precipitation SELECT * FROM catchment_precipitation(r);
end loop;
end;
$$;

--

CREATE TABLE catchment_stats_runoff(
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
insert into catchment_stats_runoff SELECT * FROM catchment_runoff(r);
end loop;
end;
$$;

--
