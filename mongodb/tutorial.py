from pymongo import MongoClient, DESCENDING

DB_NAME = "restaurants_reviews" # The name of the DB
COLLECTION_NAME = "restaurants" # The name of the collection

# Create a connection to the MongoDB
client = MongoClient("mongodb://localhost", 27017) # The protocol 'mongodb', the address 'localhost' and the port of MongoDB

db = client[DB_NAME] # Get the DB
collection = db[COLLECTION_NAME] # Get the Collection

print("Get one restaurant:")
# The find one uses to parameters, the first one {} to filter, the second {} to project the results. 
# In this case, we select everything and take all keys except the _id
res = collection.find_one({},{"_id": 0})
print(res)

print("Get one restaurants in Bronx")
# We filter restuarants by borough == Bronx
res = collection.find_one({"borough": "Bronx"},{"_id": 0})
print(res)

print("One restaurant that the score is > 90")

'''
# We select a restaurant by grades > 90 and only select the keys name and grades. 
- In this case, we only needed to indicate that we want to show the keys name and grades, 
but we didn't specify anything about the others. This is because MongoDB automatically discards
the other keys when we specify any key different from the _id .
'''
res = collection.find_one({"grades" : { "$elemMatch":{"score":{"$gt" : 90}}}},{"_id": 0,"name":1,"grades":1})
print(res)

print("Find the top 3 restaurants")
pipeline = [
    {"$unwind": "$grades"}, # Grades is a nested document that we need to unfold to access the information
    {"$group": {"_id": "$name", "avgScore": {"$avg": "$grades.score"}}}, # This is a groupby function which groups the restaurants by name and computes the avg of the grades
    {"$sort": {"avgScore": DESCENDING}}, # to order the resulting documents by avgScore in descending order
    {"$limit": 3} # To take the top 3

]

res = collection.aggregate(pipeline)

print(list(res))

print("Find a restaurant that does not do American cousine not in Brooklyn")
# It finds the restaurants that the cuisine is != American AND borough != Brooklyn
res = collection.find_one({"cuisine" : {"$ne" : "American"}, "borough": {"$ne" : "Brooklyn"}},{"_id": 0,"name":1}                    )

print(res)

client.close()
