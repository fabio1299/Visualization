DROP TABLE IF EXISTS catchment_basins;
create table catchment_basins
(
	sample_id integer not null
		constraint catchment_basins_pkey
			primary key,
	basins integer[],
	catchment geometry,
	streamlines geometry
);

create index catchment_basins_sample_id_idx
	on catchment_basins (sample_id);

do $$
   begin
    for r in 1..(SELECT COUNT(*) FROM hydrostn30_subbasin) loop
    INSERT INTO catchment_basins (sample_id, basins) VALUES
    (
     r, (SELECT array_agg(id) FROM get_catchment_table(r))
    );
    end loop;
end;
$$;

-- cache large geometry unions
UPDATE catchment_basins
SET catchment = get_catchment2(sample_id),
    streamlines = get_catchment_streamlines(sample_id)
WHERE cardinality(basins) > 2000;
