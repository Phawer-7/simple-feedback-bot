from pymongo import MongoClient


client = MongoClient("mongodb+srv://ЩЛ!")
usersdb = client.users
coll = usersdb.funtik


def createData(text: str, user_id: int, message_id: int):
    coll.insert_one({"_id": coll.count_documents({})+1, "user_id": user_id, "text": text, "message_id": message_id})


def getUser_id(message_id: int):
    return coll.find_one({"message_id": message_id})["user_id"]
