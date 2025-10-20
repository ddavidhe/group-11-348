WITH first_lap AS (
    SELECT dID, rID, time AS first_lap_time
        FROM laps
        WHERE lapNumber = 1
     ),

    first_pit AS (
        SELECT dID, rID, time AS first_pit_time
        FROM laps
        WHERE enterPitTime IS NOT NULL
        ORDER BY enterPitTime ASC
    )

SELECT (fl.first_lap_time - fp.first_pit_time) AS pit_delta FROM first_lap fl
JOIN first_pit fp ON fl.dID = fp.dID AND fl.rID = fp.rID 
WHERE fl.rID = 1 AND fl.dID = 44
ORDER BY pit_delta ASC