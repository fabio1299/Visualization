create view hydrostn30_subbasin(id, record_name, grid_value, grid_area, grid_percent, perimeter, vertex_num, basin_id, stream_order, from_x_coord, from_y_coord, to_x_coord, to_y_coord, cell_id, basin_name, "order", color, number_of_cells, stn_mainstem_length, stn_catchment_area, stn_interstation_area, next_station, geom) as
SELECT "Subbasin"."ID"                  AS id,
       "Subbasin"."RecordName"          AS record_name,
       "Subbasin"."GridValue"           AS grid_value,
       "Subbasin"."GridArea"            AS grid_area,
       "Subbasin"."GridPercent"         AS grid_percent,
       "Subbasin"."Perimeter"           AS perimeter,
       "Subbasin"."VertexNum"           AS vertex_num,
       "Subbasin"."BasinID"             AS basin_id,
       "Subbasin"."StreamOrder"         AS stream_order,
       "Subbasin"."FromXCoord"          AS from_x_coord,
       "Subbasin"."FromYCoord"          AS from_y_coord,
       "Subbasin"."ToXCoord"            AS to_x_coord,
       "Subbasin"."ToYCoord"            AS to_y_coord,
       "Subbasin"."CellID"              AS cell_id,
       "Subbasin"."BasinName"           AS basin_name,
       "Subbasin"."Order"               AS "order",
       "Subbasin"."Color"               AS color,
       "Subbasin"."NumberOfCells"       AS number_of_cells,
       "Subbasin"."STNMainstemLength"   AS stn_mainstem_length,
       "Subbasin"."STNCatchmentArea"    AS stn_catchment_area,
       "Subbasin"."STNInterStationArea" AS stn_interstation_area,
       "Subbasin"."NextStation"         AS next_station,
       "Subbasin".geom
FROM "HydroSTN30"."Subbasin";

create view hydrostn30_streamline(id, basin_id, stream_order, color, next_station, geom) as
SELECT "Streamline"."ID"          AS id,
       "Streamline"."BasinID"     AS basin_id,
       "Streamline"."StreamOrder" AS stream_order,
       "Streamline"."Color"       AS color,
       "Streamline"."NextStation" AS next_station,
       "Streamline".geom
FROM "HydroSTN30"."Streamline";



