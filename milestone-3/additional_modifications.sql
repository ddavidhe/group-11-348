ALTER TABLE races ADD FULLTEXT(trackName, trackCountry);
ALTER TABLE drivers ADD FULLTEXT(firstName, lastName);