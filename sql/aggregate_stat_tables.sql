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
SELECT "SampleID" as subbasini_d ,"Date" as date,"Year" as year,"Month" as month,"ZonalMean" as zonal_mean,"ZonalMin" as zonal_min,"ZonalMax" as zonal_max,"ZoneArea" as zone_area,'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."AirTemperature_Confluences_monthly"
ORDER BY
    subbasin_id,
    date
;








--
-- DROP MATERIALIZED VIEW air_temperature_subbasin_monthly;
-- CREATE MATERIALIZED VIEW air_temperature_subbasin_monthly
-- AS
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'Terraclimate' as model_name From "TerraClimate"."AirTemperature_Subbasin_monthly"
-- UNION
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."AirTemperature_Subbasin_monthly"
-- UNION
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."AirTemperature_Subbasin_monthly"
-- ORDER BY
--     "SampleID",
--     "Date"
-- WITH DATA;
--
-- --
--
-- DROP MATERIALIZED VIEW evapotranspiration_subbasin_monthly;
-- CREATE MATERIALIZED VIEW evapotranspiration_subbasin_monthly
-- AS
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'Terraclimate' as model_name From "TerraClimate"."Evapotranspiration_Subbasin_monthly"
-- UNION
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Evapotranspiration_Subbasin_monthly"
-- UNION
-- SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Evapotranspiration_Subbasin_monthly"
-- ORDER BY
--     "SampleID",
--     "Date"
-- WITH DATA;
