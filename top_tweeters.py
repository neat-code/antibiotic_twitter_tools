from pymongo import MongoClient

db_input = raw_input("DB name: ")
collection_input = raw_input("Collection name: ")

client = MongoClient("mongodb://localhost:27017")
db = client[db_input]
collection = db[collection_input]

result = collection.aggregate([
		{ "$group" : { "_id": "$user.screen_name",
			"count" : { "$sum": 1 }}},
		{ "$sort" : { "count" : -1 }},
		{ "$limit" : 10 }])

for document in result:
	print(document)

