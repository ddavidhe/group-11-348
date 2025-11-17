CREATE INDEX ResultsRaceIndex ON results(rID);
CREATE INDEX ResultsDriverConstructorRaceIndex ON results(dID, cID, rID);
CREATE INDEX ResultsFinishPosIndex ON results(finishPos);
CREATE INDEX ResultsRaceFinishPosIndex ON results(rID, finishPos);
