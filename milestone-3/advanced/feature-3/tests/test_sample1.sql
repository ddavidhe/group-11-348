DROP VIEW IF EXISTS constructor_master;

CREATE VIEW constructor_master AS
SELECT
    c.cID,
    c.name,
    d.lastName AS driverLastName,
    d.firstName AS driverFirstName,
    r.rID,
    r.trackName,
    res.startPos,
    res.finishPos
    FROM constructors c
    JOIN results res ON c.cID = res.cID
    JOIN races r ON res.rID = r.rID
    JOIN drivers d ON res.dID = d.dID;


SELECT c.rID, c.trackName,
c.driverLastName, c.driverFirstName, c.startPos, c.finishPos,
c2.driverLastName, c2.driverFirstName, c2.startPos, c2.finishPos,
(c2.finishPos - c.finishPos) AS finishDelta FROM constructor_master c
JOIN constructor_master c2 ON c.rID = c2.rID AND c.cID != c2.cID
WHERE c.cID = 1 AND c2.cID = 2
ORDER BY c.driverLastName ASC, c2.driverLastName ASC, c.rID ASC;