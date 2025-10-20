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
    lID INT PRIMARY KEY,
    rID INT,
    dID INT,
    lapNumber INT,
    time INT, -- seconds
    UNIQUE (rID, dID, lapNumber)
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
