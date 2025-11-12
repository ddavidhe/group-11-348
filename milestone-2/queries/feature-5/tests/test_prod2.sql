START TRANSACTION;

UPDATE results
SET finishPos = finishPos - 1
WHERE rID = 1100
AND finishPos > (
    SELECT finishPos FROM (
        SELECT finishPos
        FROM results
        WHERE dID = 830 AND cID = 131 AND rID = 1100
    ) AS dqpos
);

UPDATE results
SET finishPos = (
    SELECT COUNT(*) FROM (SELECT * FROM results) AS tmp WHERE rID = 1100
)
WHERE dID = 830 AND cID = 131 AND rID = 1100;

COMMIT;
