/* All Tweets */
SELECT VALUE COUNT(1) FROM c

/* Tweets Without Keywords */
SELECT VALUE COUNT(1) FROM c WHERE c.aboutVirus = false and c.aboutResistance = false and c.aboutCorona = false

/* Virus Tweets */
SELECT VALUE COUNT(1) FROM c WHERE c.aboutVirus = true

/* Resistance Tweets */
SELECT VALUE COUNT(1) FROM c WHERE c.aboutResistance = true

/* Corona Tweets */
SELECT VALUE COUNT(1) FROM c WHERE c.aboutCorona = true