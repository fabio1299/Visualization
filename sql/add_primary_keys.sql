-- ALTER TABLE catchment_stats_evapotranspiration ADD COLUMN id SERIAL PRIMARY KEY;
-- ALTER TABLE catchment_stats_air_temperature ADD COLUMN id SERIAL PRIMARY KEY;
-- ALTER TABLE catchment_stats_precipitation ADD COLUMN id SERIAL PRIMARY KEY;
-- ALTER TABLE catchment_stats_soil_moisture ADD COLUMN id SERIAL PRIMARY KEY;
-- ALTER TABLE catchment_stats_runoff ADD COLUMN id SERIAL PRIMARY KEY;
--
-- ALTER TABLE subbasin_evapotranspiration_monthly ADD COLUMN id SERIAL PRIMARY KEY;

CREATE INDEX ON subbasin_air_temperature_monthly(SampleID);
CREATE INDEX ON subbasin_soil_moisture_monthly(SampleID);
CREATE INDEX ON subbasin_runoff_monthly(SampleID);
CREATE INDEX ON subbasin_precipitation_monthly(SampleID);
CREATE INDEX ON subbasin_evapotranspiration_monthly(SampleID);

ALTER TABLE subbasin_air_temperature_monthly ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE subbasin_precipitation_monthly ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE subbasin_runoff_monthly ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE subbasin_soil_moisture_monthly ADD COLUMN id SERIAL PRIMARY KEY;
AlTER TABLE confluence_discharge_monthly ADD COLUMN id SERIAL PRIMARY KEY;




