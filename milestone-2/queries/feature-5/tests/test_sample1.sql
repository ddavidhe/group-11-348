START TRANSACTION;

UPDATE results
SET finishPos = finishPos - 1
WHERE rID = 1
AND finishPos > (
    SELECT finishPos FROM (
        SELECT finishPos
        FROM results
        WHERE dID = 44 AND cID = 8 AND rID = 1
    ) AS dqpos
);

UPDATE results
SET finishPos = (
    SELECT COUNT(*) FROM (SELECT * FROM results) AS tmp WHERE rID = 1
)
WHERE dID = 44 AND cID = 8 AND rID = 1;

COMMIT;
