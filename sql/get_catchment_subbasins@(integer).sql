create function get_catchment_subbasins(integer)
    returns TABLE("ID" integer, "RecordName" character varying, "GridValue" integer, "GridArea" double precision, "GridPercent" double precision, "Perimeter" double precision, "VertexNum" integer, "BasinID" integer, "StreamOrder" integer, "FromXCoord" double precision, "FromYCoord" double precision, "ToXCoord" double precision, "ToYCoord" double precision, "CellID" integer, "BasinName" character varying, "Order" integer, "Color" integer, "NumberOfCells" integer, "STNMainstemLength" double precision, "STNCatchmentArea" double precision, "STNInterStationArea" double precision, "NextStation" integer, geom geometry)
    language plpgsql
as
$$
    #variable_conflict use_column
    DECLARE
        subbasin_id alias for $1;
    BEGIN
         RETURN QUERY SELECT * FROM "HydroSTN30"."Subbasin" WHERE "ID" IN
                                                    (SELECT unnest(basins) from catchment_basins_test where sample_id = subbasin_id);
END;
$$;

alter function get_catchment_subbasins(integer) owner to danielv;

