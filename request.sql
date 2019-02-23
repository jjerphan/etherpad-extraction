SELECT `key`, value
FROM store
WHERE `key` NOT LIKE "sessionstorage:%"
AND   `key` NOT LIKE "token2author:%"
AND   `key` NOT LIKE "pad:%:revs:%"
AND   `key` NOT LIKE "%readonly%"
INTO OUTFILE '/var/lib/dump.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
