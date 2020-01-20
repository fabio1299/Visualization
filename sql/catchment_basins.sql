
DROP TABLE catchment_basins;
CREATE TABLE catchment_basins(
--  subbasin
    sample_id integer PRIMARY KEY,
--  Array of subbasins making up corresponding catchment
    basins integer []
);

do $$
begin
for r in 1..48077 loop

    INSERT INTO catchment_basins (sample_id, basins) VALUES
    (
     r, (SELECT array_agg(id) FROM get_catchment_table(r))
    );


end loop;
end;
$$;