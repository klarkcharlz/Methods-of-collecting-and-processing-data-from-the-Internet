def mongo_update_without_duplicate(collection, filter_, data):
    collection.update_one(filter_, data, upsert=True)


def find_interested_vacancy(collection, min_salary):
    interested_vacancy = collection.find({"$or": [{"min_salary": {"$gte": min_salary}},
                                                  {"max_salary": {"$gte": min_salary}}]})
    return list(interested_vacancy)
