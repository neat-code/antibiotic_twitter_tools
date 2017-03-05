from pymongo import MongoClient

db_input = raw_input("Enter DB: ")
db_collection = raw_input("Enter collection: ")

client = MongoClient("mongodb://localhost:27017")
db = client[db_input]
collection = db[db_collection]

result = collection.aggregate([{
        "$group" : {
            "_id" : {
                "day" : {
                    "$dayOfMonth" : "$created_at" 
                },
		"month": {
                    "$month" : "$created_at"
                },
                "year" : {
                    "$year" : "$created_at" 
                },
            },
            "totalReTweetsPerDay" : {
                "$sum" : {
                    "$cond" : [{
                        "$ifNull" : ["$retweeted_status.id", "false"]
                    }, 1, 0]
                }
            },
            "totalTweetsPerDay" : {
                "$sum": 1
            }
        }
    }, {
        "$sort": {
            "_id": -1
        }
    }, {
        "$out": "daily_tweets"
    }]
)

print(result)
