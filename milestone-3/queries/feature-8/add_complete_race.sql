-- Feature 8: Add Complete Race with Results and Laps
-- This adds a complete race in a single atomic transaction

START TRANSACTION;

-- Insert race information
INSERT INTO races (rID, trackName, trackCountry, round, season)
VALUES ({rID}, '{trackName}', '{trackCountry}', {round}, {season});

-- Batch insert results
-- Format: (rID, dID, cID, startPos, finishPos)
{results_insert}

-- Batch insert laps (optional)
-- Format: (rID, dID, lapNumber, time, standing, finishTime, enterPitTime, exitPitTime)
{laps_insert}

COMMIT;
