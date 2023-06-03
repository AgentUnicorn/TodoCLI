from pymongo import MongoClient
from bson.objectid import ObjectId
from rich.console import Console

console = Console()

def get_datebase():
    CONNECTION_STRING = "mongodb://localhost:27017"

    client = MongoClient(CONNECTION_STRING)
    return client['todocli_py']

if __name__ == "__main__":
    dbname = get_datebase()