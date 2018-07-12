from pymongo import MongoClient

client = MongoClient()
# "mongodb://localhost:21017"

db = client.test

# cursor = db.restaurants.find()

# for document in cursor:
#     print(document)

# cursor1 = db.restaurants.find({"borough": "Manhattan"})

# for document in cursor1:
#     print(document)

# cursor_gt30 = db.restaurants.find({"grades.score": {"$gt": 30}})

# for document in cursor_gt30:
#     print(document)

# cursor_italia_gt30 = db.restaurants.find(
#     {"$and": [{"cuisine": "Italian"}, {"grades.score": {"$gt": 30}}]})

# for document in cursor_italia_gt30:
#     print(document)

# cursor = db.restaurants.aggregate(
#     [
#         {"$match": {"borough": "Queens", "cuisine": "Brazilian"}},
#         {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}}
#     ]
# )

cursor = db.restaurants.aggregate(
    [
        {"$match": {"cuisine": "Chinese"}},
        {"$group": {"_id": "$address.zipcode",
                    "count": {"$sum": 1}
                  # , "avg": {"$avg": "$grades.score"}
                    }
        }
    ]
)

for document in cursor:
    print(document)
