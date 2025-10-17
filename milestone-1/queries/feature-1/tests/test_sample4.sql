SELECT firstName, lastName, driverTag, SUM(points.number) AS points
    FROM (results NATURAL JOIN races JOIN points ON results.finishPos = points.position AND races.season = points.season)
        RIGHT OUTER JOIN drivers ON drivers.dID = results.dID
    WHERE round >= 1 AND round <= 22 AND races.season = 2026
    GROUP BY drivers.dID, firstName, lastName, driverTag ORDER BY points DESC;