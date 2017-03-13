# antibiotic_twitter_tools
Scripts for data analysis of gathered tweets.

## Date conversion
Since the timestamp of the tweets were saved as a string in the same format as provided by Twitter, the database had to be updated with the timestamp converted to Date-format.

### Use
`mongo [mongo-instance]/[database] --eval 'collection = db.getCollection("[collection]")' date_conversion.js`

## Day count
Counts all tweets by date.
### Use
`mongo [mongo-instance]/[database] --eval 'collection = db.getCollection("[collection]")' day_count.js`

