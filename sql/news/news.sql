DROP TABLE NETWORK;
CREATE TABLE NETWORK
(
    id serial NOT NULL,
    name varchar(100),
    to_cell integer,
    from_cell integer,
    "order" integer,
    basin_id integer,
    basin_cells integer,
    travel integer,
    cell_area double precision,
    cell_length double precision,
    subbasin_area double precision,
    subbasin_length double precision,
    cell_x_coord double precision,
    cell_y_coord double precision,
    dist_to_mouth double precision,
    dist_to_ocean double precision
);

-- skip header, tab delimited, NA values = empty string
COPY network(
             id, name, to_cell, from_cell, "order", basin_id, basin_cells, travel, cell_area, cell_length,
             subbasin_area, subbasin_length, cell_x_coord, cell_y_coord, dist_to_mouth, dist_to_ocean
            )
FROM PROGRAM 'tail -n +2 /asrc/ecr/NEWS/Visualization/Network/NetworkWithDistance.txt' DELIMITER E'\t' NULL '';

