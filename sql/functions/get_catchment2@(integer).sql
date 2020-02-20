create or replace function get_catchment2(integer) returns geometry
    immutable
    strict
    parallel safe
    language plpgsql
as
$$
DECLARE
    basinid alias for $1;
    catch    geometry;
BEGIN

SELECT * FROM st_union((SELECT array_agg(geom)
FROM "HydroSTN30"."Subbasin"
WHERE "ID" IN (SELECT unnest(basins) from catchment_basins where sample_id = basinid) ))
INTO catch;
RETURN catch;
END;
$$;
