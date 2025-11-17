START TRANSACTION;

UPDATE results
SET finishPos = finishPos - 1
WHERE rID = {rID}
AND finishPos > (
    SELECT finishPos FROM (
        SELECT finishPos
        FROM results
        WHERE dID = {dID} AND cID = {cID} AND rID = {rID}
    ) AS dqpos
);

UPDATE results
SET finishPos = (
    SELECT COUNT(*) FROM (SELECT * FROM results) AS tmp WHERE rID = {rID}
)
WHERE dID = {dID} AND cID = {cID} AND rID = {rID};

COMMIT;
