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
    country VARCHAR(100) NOT NULL,
    age INT NOT NULL
);

CREATE TABLE constructors (
    cID INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start DATE,
    end DATE
);

CREATE TABLE races (
    rID INT PRIMARY KEY,
    trackName VARCHAR(100) NOT NULL,
    trackCountry VARCHAR(100) NOT NULL,
    raceNumber INT NOT NULL,
    season INT NOT NULL
);

CREATE TABLE stints (
    dID INT,
    cID INT,
    sID INT,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    PRIMARY KEY (dID, cID, sID),
    FOREIGN KEY (dID) REFERENCES drivers(dID),
    FOREIGN KEY (cID) REFERENCES constructors(cID)
);

CREATE TABLE lap_telemetries (
    rID INT,
    lapNumber INT,
    rainFall BOOL,
    windSpeed FLOAT,
    trackTemp FLOAT,
    airTemp FLOAT,
    PRIMARY KEY (rID, lapNumber),
    FOREIGN KEY (rID) REFERENCES races(rID)
);