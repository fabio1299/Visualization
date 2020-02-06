
--
DROP MATERIALIZED VIEW air_temperature_subbasin_monthly;
CREATE MATERIALIZED VIEW air_temperature_subbasin_monthly
AS
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'Terraclimate' as model_name From "TerraClimate"."AirTemperature_Subbasin_monthly"
UNION
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."AirTemperature_Subbasin_monthly"
UNION
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."AirTemperature_Subbasin_monthly"
ORDER BY
    "SampleID",
    "Date"
WITH DATA;

--

DROP MATERIALIZED VIEW evapotranspiration_subbasin_monthly;
CREATE MATERIALIZED VIEW evapotranspiration_subbasin_monthly
AS
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'Terraclimate' as model_name From "TerraClimate"."Evapotranspiration_Subbasin_monthly"
UNION
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Evapotranspiration_Subbasin_monthly"
UNION
SELECT "SampleID","Date","Year","Month","ZonalMean","ZonalMin","ZonalMax","ZoneArea",'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Evapotranspiration_Subbasin_monthly"
ORDER BY
    "SampleID",
    "Date"
WITH DATA;
