WITH finishPositions AS (
  SELECT rID, dID, lapNumber - 1 AS lapNumber, standing AS finishPos
  FROM laps
  WHERE lapNumber > 1
  UNION
  SELECT rID, dID, (SELECT MAX(lapNumber) FROM laps WHERE rID = 1116) AS lapNumber, finishPos
  FROM results
)
SELECT firstName, lastName, driverTag, time, standing AS startPos, finishPos
FROM laps
LEFT OUTER JOIN finishPositions
ON laps.rID = finishPositions.rID
  AND laps.dID = finishPositions.dID
  AND laps.lapNumber = finishPositions.lapNumber
JOIN drivers
ON laps.dID = drivers.dID
WHERE laps.rID = 1116
  AND laps.lapNumber = 10
ORDER BY finishPos, startPos;
