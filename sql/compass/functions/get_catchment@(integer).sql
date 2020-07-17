create function get_catchment(integer) returns geometry
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
    --- basinCTE is a table containing all upstream hydrostn30_subbasin rows
    WITH RECURSIVE basinCTE as (
        -- Anchor
        SELECT hydrostn30_subbasin.id, hydrostn30_subbasin.next_station, hydrostn30_subbasin."geom"
        FROM hydrostn30_subbasin
        WHERE hydrostn30_subbasin.id = basinid

        UNION ALL
        -- Recursive
        SELECT hydrostn30_subbasin.id, hydrostn30_subbasin.next_station, hydrostn30_subbasin."geom"
        FROM hydrostn30_subbasin
                 JOIN basinCTE
                      ON hydrostn30_subbasin.next_station = basinCTE.id --- switch to get downstream subbasin instead
    )
	
	---Force Right Hand Rule and join Geometries
    SELECT ST_ForceRHR(st_union(basinCTE.geom)) AS catch1
    FROM basinCTE
    INTO catch;
    RETURN catch;
END;
$$;

alter function get_catchment(integer) owner to danielv;

