DROP TABLE IF EXISTS catchment_stats_air_temperature;
create table catchment_stats_air_temperature
(
	subbasin_id integer,
	date varchar(10),
	model_name text,
	mean_zonal_mean double precision,
	mean_zonal_min double precision,
	mean_zonal_max double precision,
	id serial not null
		constraint catchment_stats_air_temperature_pkey
			primary key
);
create index catchment_stats_air_temperature_subbasin_id_idx
	on catchment_stats_air_temperature (subbasin_id);

DROP TABLE IF EXISTS catchment_stats_evapotranspiration;
create table catchment_stats_evapotranspiration
(
	subbasin_id integer,
	date varchar(10),
	model_name text,
	mean_zonal_mean double precision,
	mean_zonal_min double precision,
	mean_zonal_max double precision,
	id serial not null
		constraint catchment_stats_evapotranspiration_pkey
			primary key
);
create index catchment_stats_evapotranspiration_subbasin_id_idx
	on catchment_stats_evapotranspiration (subbasin_id);

DROP TABLE IF EXISTS catchment_stats_precipitation;
create table catchment_stats_precipitation
(
	subbasin_id integer,
	date varchar(10),
	model_name text,
	mean_zonal_mean double precision,
	mean_zonal_min double precision,
	mean_zonal_max double precision,
	id serial not null
		constraint catchment_stats_precipitation_pkey
			primary key
);
create index catchment_stats_precipitation_subbasin_id_idx
	on catchment_stats_precipitation (subbasin_id);

DROP TABLE IF EXISTS catchment_stats_runoff;
create table catchment_stats_runoff
(
	subbasin_id integer,
	date varchar(10),
	model_name text,
	mean_zonal_mean double precision,
	mean_zonal_min double precision,
	mean_zonal_max double precision,
	id serial not null
		constraint catchment_stats_runoff_pkey
			primary key
);
create index catchment_stats_runoff_subbasin_id_idx
	on catchment_stats_runoff (subbasin_id);

DROP TABLE IF EXISTS catchment_stats_soil_moisture;
create table catchment_stats_soil_moisture
(
	subbasin_id integer,
	date varchar(10),
	model_name text,
	mean_zonal_mean double precision,
	mean_zonal_min double precision,
	mean_zonal_max double precision,
	id serial not null
		constraint catchment_stats_soil_moisture_pkey
			primary key
);
create index catchment_stats_soil_moisture_subbasin_id_idx
	on catchment_stats_soil_moisture (subbasin_id);

do $$
begin
for r in 1..(SELECT COUNT(*) FROM hydrostn30_subbasin) loop
    insert into catchment_stats_air_temperature SELECT * FROM catchment_air_temperature(r);
    insert into catchment_stats_evapotranspiration SELECT * FROM catchment_evapotranspiration(r);
    insert into catchment_stats_precipitation SELECT * FROM catchment_precipitation(r);
    insert into catchment_stats_runoff SELECT * FROM catchment_runoff(r);
    insert into catchment_stats_soil_moisture SELECT * FROM catchment_soil_moisture(r);
end loop;
end;
$$;



