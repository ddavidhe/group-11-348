CREATE INDEX LapsRaceIndex ON laps(rID);
CREATE INDEX LapsLapNumberIndex ON laps(lapNumber);
CREATE INDEX LapsRaceLapNumberIndex ON laps(rID, lapNumber);
CREATE INDEX LapsLapNumberRaceIndex ON laps(lapNumber, rID);
