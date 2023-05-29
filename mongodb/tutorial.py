from pymongo import MongoClient, DESCENDING

DB_NAME = "restaurants_reviews"
COLLECTION_NAME = "restaurants"


client = MongoClient("mongodb://localhost", 27017)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("Get one restaurant:")
res = collection.find_one({},{"_id": 0})
print(res)

print("Get one restaurants in Bronx")
res = collection.find_one({"borough": "Bronx"},{"_id": 0})
print(res)

print("One restaurant that the score is > 90")
res = collection.find_one({"grades" : { "$elemMatch":{"score":{"$gt" : 90}}}},{"_id": 0,"name":1,"grades":1})
print(res)

print("Find the top restaurants")
pipeline = [
    {"$unwind": "$grades"},
    {"$group": {"_id": "$name", "avgScore": {"$avg": "$grades.score"}}},
    {"$sort": {"avgScore": DESCENDING}},
    {"$limit": 3}

]

res = collection.aggregate(pipeline)

print(list(res))

print("Find a restaurant that does not do American cousine not in Brooklyn")
res = collection.find_one({"cuisine" : {"$ne" : "American"}, "borough": {"$ne" : "Brooklyn"}},{"_id": 0,"name":1}                    )

print(res)

client.close()
