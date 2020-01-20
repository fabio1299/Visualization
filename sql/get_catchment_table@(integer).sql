create function get_catchment_table(basinid integer) returns SETOF hydrostn30_subbasin
    language sql
as
$$
WITH RECURSIVE basinCTE as(
        -- Anchor
        SELECT  *
        FROM hydrostn30_subbasin
        WHERE hydrostn30_subbasin.id = basinid

        UNION ALL
        -- Recursive
        SELECT hydrostn30_subbasin.*
        FROM hydrostn30_subbasin
                 JOIN basinCTE
                      ON hydrostn30_subbasin.next_station = basinCTE.id --- switch to get downstream subbasin instead
    )
    SELECT * FROM basinCTE;
$$;

alter function get_catchment_table(integer) owner to danielv;

