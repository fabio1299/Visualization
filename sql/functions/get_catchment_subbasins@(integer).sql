create or replace function get_catchment_subbasins(integer)
    returns TABLE("ID" integer, geom geometry)
    language plpgsql
as
$$
    #variable_conflict use_column
    DECLARE
        subbasin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT "ID", geom FROM "HydroSTN30"."Subbasin" WHERE "ID" IN
                                                    (SELECT unnest(basins) from catchment_basins where sample_id = subbasin_id);
END;
$$;

alter function get_catchment_subbasins(integer) owner to danielv;

