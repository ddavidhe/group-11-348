CREATE INDEX LapsRaceIndex ON laps(rID);
CREATE INDEX LapsDriverIndex ON laps(dID);
CREATE INDEX LapsRaceDriverIndex ON laps(rID, dID);
CREATE INDEX LapsDriverRaceIndex ON laps(dID, rID);
