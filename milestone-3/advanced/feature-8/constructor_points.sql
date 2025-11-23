SELECT /*+ HASH_JOIN(r c ra p) */
       r.cID,
       c.name,
       SUM(p.number) AS total_points
FROM results AS r
LEFT JOIN constructors AS c
    ON r.cID = c.cID
JOIN races AS ra
    ON r.rID = ra.rID
LEFT JOIN points AS p
    ON r.finishPos = p.position
   AND ra.season = p.season
GROUP BY r.cID, c.name
ORDER BY total_points DESC;
