CREATE MATERIALIZED VIEW network_paths as
    SELECT "ID",news_geom_to_mouth("ID"::int) FROM network_with_geometry;

DROP FUNCTION news_get_time_series(start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION);
CREATE OR REPLACE FUNCTION news_get_time_series (start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION)
	RETURNS TABLE (
		year INT,
		day_of_year INT,
		--measurement DOUBLE PRECISION
		measurement float8,
		point geometry
)
AS $$
DECLARE
    thepoint geometry := ST_Setsrid(ST_Point(longitude,latitude),4326);
BEGIN
RETURN QUERY
    with myresult as(
        with myclip as (
            SELECT air_temp.rid,st_clip(air_temp.rast, thepoint) as clip,air_temp.year
                FROM air_temperature_50x50 air_temp
            WHERE ST_Intersects(air_temp.rast, thepoint)
                AND air_temp.year BETWEEN start_year AND end_year
        )
        SELECT (st_dumpvalues(clip)).*,myclip.year from myclip
    )
    -- SELECT myresult.year,myresult.nband as day_of_year,unnest(valarray[1:1][1]) as measurement FROM myresult;
    SELECT myresult.year,myresult.nband as day_of_year,unnest(valarray[1:1][1]) as measurement, thepoint as point FROM myresult;
END; $$
LANGUAGE 'plpgsql'
PARALLEL SAFE;

--
DROP FUNCTION news_get_watertemp(start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION);
CREATE OR REPLACE FUNCTION news_get_watertemp (start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION)
	RETURNS TABLE (
		year INT,
		day_of_year INT,
		--measurement DOUBLE PRECISION
		measurement float8,
        coord_id text
)
AS $$
DECLARE
    thepoint geometry := ST_Setsrid(ST_Point(longitude,latitude),4326);
BEGIN
RETURN QUERY
    with myresult as(
        with myclip as (
            SELECT watertemp.rid,st_clip(watertemp.rast, thepoint) as clip,watertemp.year
                FROM qxt_watertemp watertemp
            WHERE ST_Intersects(watertemp.rast, thepoint)
                AND watertemp.year BETWEEN start_year AND end_year
        )
        SELECT (st_dumpvalues(clip)).*,myclip.year from myclip
    )
    SELECT myresult.year,myresult.nband as day_of_year,unnest(valarray[1:1][1]) as measurement,
            concat(longitude::text,'_',latitude::text) as coord_id FROM myresult;
END; $$
LANGUAGE 'plpgsql'
PARALLEL SAFE;
--
--
--

DROP FUNCTION news_get_watertemp2(start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION);
CREATE OR REPLACE FUNCTION news_get_watertemp2 (start_year INT, end_year INT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION)
	RETURNS TABLE (
		year INT,
		day_of_year INT,
		--measurement DOUBLE PRECISION
		measurement float8,
		point geometry,
		long double precision,
		lat double precision,
		dist2mouth double precision
)
AS $$
DECLARE
    thepoint geometry := ST_Setsrid(ST_Point(longitude,latitude),4326);
BEGIN
RETURN QUERY
    with myresult as(
        with myclip as (
            SELECT watertemp.rid,st_clip(watertemp.rast, thepoint) as clip,watertemp.year, longitude as long,
                   latitude as lat
                FROM qxt_watertemp watertemp
            WHERE ST_Intersects(watertemp.rast, thepoint)
                AND watertemp.year BETWEEN start_year AND end_year
        )
        SELECT (st_dumpvalues(clip)).*,myclip.year, myclip.long, myclip.lat from myclip
    )
    SELECT myresult.year,myresult.nband as day_of_year,unnest(valarray[1:1][1]) as measurement, thepoint as point,
           myresult.long, myresult.lat, net."Dist2Mouth"
    FROM myresult LEFT JOIN network_with_geometry net ON st_dwithin(thepoint,net.point,.0023);
END; $$
LANGUAGE 'plpgsql'
PARALLEL SAFE;

--
--
--
--

DROP FUNCTION news_get_time_series(start_year INT, end_year INT, geom geometry);
CREATE OR REPLACE FUNCTION news_get_time_series (start_year INT, end_year INT, geom geometry)
	RETURNS TABLE (
		year INT,
		day_of_year INT,
		measurement float8[]
)
AS $$
BEGIN
RETURN QUERY
    with myresult as(
        with myclip as (
            SELECT air_temp.rid,st_clip(ST_setsrid(air_temp.rast,4326), geom) as clip,air_temp.year
                FROM air_temperature_50x50 air_temp
            WHERE ST_Intersects(ST_setsrid(air_temp.rast,4326), geom)
                AND air_temp.year BETWEEN start_year AND end_year
        )
        SELECT (st_dumpvalues(clip)).*,myclip.year from myclip
    )
    SELECT myresult.year,myresult.nband as day_of_year,valarray as measurement FROM myresult;
END; $$
LANGUAGE 'plpgsql';

--
--

DROP FUNCTION news_path_to_mouth;
CREATE OR REPLACE FUNCTION news_path_to_mouth(start_id INT)
RETURNS TABLE
(
-- 	index bigint,
	"ID" bigint,
	"ID_To" bigint,
-- 	"Name" text,
-- 	"ToCell" bigint,
-- 	"FromCell" double precision,
-- 	"Order" bigint,
	"BasinID" bigint,
-- 	"BasinCells" bigint,
-- 	"Travel" bigint,
-- 	"CellArea" double precision,
-- 	"CellLength" double precision,
-- 	"SubbasArea" double precision,
-- 	"SubbaLengh" double precision,
	longitude double precision,
	latitude double precision,
	coord_id text,
	"Dist2Mouth" double precision,
	"Dist2Ocean" double precision,
	point geometry(Point,4326)
-- 	line geometry(LineString,4326)
)
AS $$
    BEGIN
        RETURN QUERY
            WITH RECURSIVE path AS(
                SELECT
                       n1."ID",
                       n1."ID_To",
                       n1."BasinID",
                       n1."CellXCoord" as longtitude,
                       n1."CellYCoord" as latitude,
                       n1.coord_id,
                       n1."Dist2Mouth",
                       n1."Dist2Ocean",
                       n1.point

                FROM
                    network_with_geometry n1
                WHERE
                    n1."ID" = start_id
                UNION
                    SELECT
                        n."ID",
                       n."ID_To",
                       n."BasinID",
                       n."CellXCoord" as longitude,
                       n."CellYCoord" as latitude,
                       n.coord_id,
                       n."Dist2Mouth",
                       n."Dist2Ocean",
                       n.point
                    FROM network_with_geometry n
                    INNER JOIN path p ON p."ID_To"=n."ID"
            ) SELECT * FROM path;
    end;
    $$
LANGUAGE 'plpgsql'
PARALLEL SAFE;

CREATE OR REPLACE FUNCTION news_geom_to_mouth(start_id INT)
RETURNS geometry
AS $$
BEGIN
    Return (SELECT ST_Union(point) FROM news_path_to_mouth(start_id));
end;
    $$
LANGUAGE 'plpgsql'
PARALLEL SAFE;
