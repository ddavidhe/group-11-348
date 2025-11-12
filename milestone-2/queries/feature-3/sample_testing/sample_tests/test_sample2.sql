WITH first_lap AS (
    SELECT dID, rID, time AS first_lap_time
        FROM laps
        WHERE lapNumber = 1
     ),

    pits AS (
        SELECT dID, rID, lapNumber, time AS pit_times
        FROM laps
        WHERE enterPitTime IS NOT NULL
    )

SELECT p.lapNumber as pit_lap_number,
fl.first_lap_time,
p.pit_times,
(fl.first_lap_time - p.pit_times) AS pit_delta
FROM first_lap fl
JOIN pits p ON fl.dID = p.dID AND fl.rID = p.rID 
WHERE fl.rID = 13 AND fl.dID = 16

UNION ALL

SELECT 
    1 AS pit_lap_number,
    fl.first_lap_time,
    NULL AS pit_time,
    NULL AS pit_delta
FROM first_lap fl
WHERE fl.rID = 13 
  AND fl.dID = 16

ORDER BY pit_lap_number ASC;
