SELECT c.rID, c.trackName,
c.driverLastName, c.driverFirstName, c.startPos, c.finishPos,
c2.driverLastName, c2.driverFirstName, c2.startPos, c2.finishPos,
(c2.finishPos - c.finishPos) AS finishDelta FROM constructor_master c
JOIN constructor_master c2 ON c.rID = c2.rID AND c.cID != c2.cID
WHERE c.cID = {} AND c2.cID = {}
ORDER BY c.driverLastName ASC, c2.driverLastName ASC, c.rID ASC;