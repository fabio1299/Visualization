DROP TABLE IF EXISTS confluence_discharge_monthly;
create table public.confluence_discharge_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	discharge double precision,
	model_name text,
	id serial not null
		constraint confluence_discharge_monthly_pkey
			primary key
);

create index "confluence_discharge_monthly_SampleID_idx"
	on public.confluence_discharge_monthly (subbasin_id);

INSERT INTO confluence_discharge_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month, "Discharge" as discharge,'Terraclimate' as model_name From "TerraClimate"."Discharge_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"Discharge" as discharge,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Discharge_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"Discharge" as discharge,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Discharge_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;

DROP TABLE IF EXISTS subbasin_air_temperature_monthly;
create table subbasin_air_temperature_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	zonal_mean double precision,
	zonal_min double precision,
	zonal_max double precision,
	zone_area double precision,
	model_name text,
	id serial not null
		constraint subbasin_air_temperature_monthly_pkey
			primary key
);

create index "subbasin_air_temperature_monthly_SampleID_idx"
	on subbasin_air_temperature_monthly (subbasin_id);

INSERT INTO subbasin_air_temperature_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'Terraclimate' as model_name From "TerraClimate"."AirTemperature_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."AirTemperature_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."AirTemperature_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;

DROP TABLE IF EXISTS subbasin_evapotranspiration_monthly;
create table subbasin_evapotranspiration_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	zonal_mean double precision,
	zonal_min double precision,
	zonal_max double precision,
	zone_area double precision,
	model_name text,
	id serial not null
		constraint subbasin_evapotranspiration_monthly_pkey
			primary key
);

create index "subbasin_evapotranspiration_monthly_SampleID_idx"
	on subbasin_evapotranspiration_monthly (subbasin_id);

INSERT INTO subbasin_evapotranspiration_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'Terraclimate' as model_name From "TerraClimate"."Evapotranspiration_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Evapotranspiration_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Evapotranspiration_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;

DROP TABLE IF EXISTS subbasin_precipitation_monthly;
create table subbasin_precipitation_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	zonal_mean double precision,
	zonal_min double precision,
	zonal_max double precision,
	zone_area double precision,
	model_name text,
	id serial not null
		constraint subbasin_precipitation_monthly_pkey
			primary key
);

create index "subbasin_precipitation_monthly_SampleID_idx"
	on subbasin_precipitation_monthly (subbasin_id);

INSERT INTO subbasin_precipitation_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'Terraclimate' as model_name From "TerraClimate"."Precipitation_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Precipitation_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Precipitation_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;

DROP TABLE IF EXISTS subbasin_runoff_monthly;
create table subbasin_runoff_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	zonal_mean double precision,
	zonal_min double precision,
	zonal_max double precision,
	zone_area double precision,
	model_name text,
	id serial not null
		constraint subbasin_runoff_monthly_pkey
			primary key
);

create index "subbasin_runoff_monthly_SampleID_idx"
	on subbasin_runoff_monthly (subbasin_id);

INSERT INTO subbasin_runoff_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'Terraclimate' as model_name From "TerraClimate"."Runoff_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Runoff_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Runoff_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;

DROP TABLE IF EXISTS subbasin_soil_moisture_monthly;
create table subbasin_soil_moisture_monthly
(
	subbasin_id integer,
	date varchar(10),
	year integer,
	month integer,
	zonal_mean double precision,
	zonal_min double precision,
	zonal_max double precision,
	zone_area double precision,
	model_name text,
	id serial not null
		constraint subbasin_soil_moisture_monthly_pkey
			primary key
);

create index "subbasin_soil_moisture_monthly_SampleID_idx"
	on subbasin_soil_moisture_monthly (subbasin_id);

INSERT INTO subbasin_soil_moisture_monthly
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'Terraclimate' as model_name From "TerraClimate"."SoilMoisture_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."SoilMoisture_Confluences_monthly"
UNION
SELECT "SampleID" as subbasin_id ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."SoilMoisture_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;
