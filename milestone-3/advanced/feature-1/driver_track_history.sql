WITH driver_matches AS (SELECT dID, firstName, lastName,
       MATCH(firstName, lastName)
         AGAINST ('{}' IN NATURAL LANGUAGE MODE) AS score
FROM drivers),
race_matches AS (SELECT rID, trackName, trackCountry FROM races WHERE
       MATCH(trackName, trackCountry)
         AGAINST ('{}' IN NATURAL LANGUAGE MODE))
SELECT firstName, lastName, trackName, trackCountry, COUNT(*) AS races, AVG(startPos) AS average_quali, AVG(finishPos) AS avg_result
FROM driver_matches d JOIN results ON d.dID = results.dID JOIN race_matches r ON r.rID = results.rID
WHERE d.score != 0 AND d.score = (SELECT MAX(score) FROM driver_matches)
GROUP BY d.dID, firstName, lastName, trackName, trackCountry;