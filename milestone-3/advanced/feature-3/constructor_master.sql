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

SELECT * FROM constructor_master
WHERE cID = {}
ORDER BY driverLastName ASC, rID ASC;