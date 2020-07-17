ALTER TABLE qxt_watertemp ADD COLUMN year int;
WITH new_values as (
SELECT
	rid,CAST(SUBSTRING( filename, 18,4) AS int) AS y
FROM
	qxt_watertemp)
	UPDATE qxt_watertemp as air
SET year = new_values.y
FROM new_values
where air.rid = new_values.rid;
