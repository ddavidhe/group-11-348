CREATE TABLE points (
    season INT,
    position INT,
    number INT NOT NULL,
    PRIMARY KEY (season, position)
);

CREATE TABLE drivers (
    dID INT PRIMARY KEY,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    driverTag VARCHAR(3) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    age INT NOT NULL
);

CREATE TABLE constructors (
    cID INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE races (
    rID INT PRIMARY KEY,
    trackName VARCHAR(100) NOT NULL,
    trackCountry VARCHAR(100) NOT NULL,
    round INT NOT NULL,
    season INT NOT NULL
);

CREATE TABLE laps (
    rID INT,
    dID INT,
    lapNumber INT NOT NULL,
    standing INT NOT NULL, -- driver's position at the start of the lap
    time FLOAT NOT NULL, -- time it took for driver to complete this lap (seconds)
    finishTime FLOAT NOT NULL, -- timestamp of this lap being completed (seconds)
    enterPitTime FLOAT, -- timestamp of entering pit (seconds)
    exitPitTime FLOAT, -- timestamp of exiting pit (seconds)
    PRIMARY KEY (rID, dID, lapNumber),
    FOREIGN KEY (rID) REFERENCES races(rID),
    FOREIGN KEY (dID) REFERENCES drivers(dID)
);

CREATE TABLE weather (
    rID INT,
    time FLOAT NOT NULL, -- timestamp of the weather reading (seconds)
    rainFall BOOL NOT NULL,
    windSpeed FLOAT NOT NULL,
    trackTemperature FLOAT NOT NULL,
    airTemperature FLOAT NOT NULL,
    FOREIGN KEY (rID) REFERENCES races(rID)
);

CREATE TABLE results (
    dID INT,
    cID INT,
    rID INT,
    startPos INT NOT NULL,
    finishPos INT NOT NULL,
    PRIMARY KEY (dID, cID, rID),
    FOREIGN KEY (dID) REFERENCES drivers(dID),
    FOREIGN KEY (cID) REFERENCES constructors(cID),
    FOREIGN KEY (rID) REFERENCES races(rID)
);
