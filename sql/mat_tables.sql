
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

CREATE INDEX ON air_temperature_subbasin_monthly ("SampleID");

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

CREATE INDEX ON evapotranspiration_subbasin_monthly ("SampleID");

--

DROP MATERIALIZED VIEW discharge_confluence_monthly;
CREATE MATERIALIZED VIEW discharge_confluence_monthly
AS
    SELECT "Discharge_Conf_monthly"."SampleID","Discharge_Conf_monthly"."Date","Discharge_Conf_monthly"."Year",
           "Discharge_Conf_monthly"."Month","Discharge","ZoneArea",
           'Terraclimate' as model_name From "TerraClimate"."Discharge_Conf_monthly"
    LEFT JOIN "TerraClimate"."AirTemperature_Subbasin_monthly"
    ON "Discharge_Conf_monthly"."ID" = "AirTemperature_Subbasin_monthly"."ID"

    UNION

    SELECT "Discharge_Conf_monthly"."SampleID","Discharge_Conf_monthly"."Date","Discharge_Conf_monthly"."Year",
           "Discharge_Conf_monthly"."Month","Discharge","ZoneArea",
           'WBMprist_CRUTSv401' as model_name From "WBMprist_CRUTSv401"."Discharge_Conf_monthly"
    LEFT JOIN "WBMprist_CRUTSv401"."AirTemperature_Subbasin_monthly"
    ON "Discharge_Conf_monthly"."ID" = "AirTemperature_Subbasin_monthly"."ID"
    UNION

    SELECT "Discharge_Conf_monthly"."SampleID","Discharge_Conf_monthly"."Date","Discharge_Conf_monthly"."Year",
           "Discharge_Conf_monthly"."Month","Discharge","ZoneArea",
           'WBMprist_GPCCv7' as model_name From "WBMprist_GPCCv7"."Discharge_Conf_monthly"
    LEFT JOIN "WBMprist_GPCCv7"."AirTemperature_Subbasin_monthly"
    ON "Discharge_Conf_monthly"."ID" = "AirTemperature_Subbasin_monthly"."ID"

ORDER BY
    "SampleID",
    "Date"
WITH DATA;

CREATE INDEX ON discharge_confluence_monthly ("SampleID");

-- Hasura doesn't support Materialized Views, these "redirect views" gives Hasura Access
CREATE VIEW air_temperature_subbasin_monthly_ as SELECT * FROm air_temperature_subbasin_monthly;
CREATE VIEW evapotranspiration_subbasin_monthly_ as SELECT * FROM evapotranspiration_subbasin_monthly;

