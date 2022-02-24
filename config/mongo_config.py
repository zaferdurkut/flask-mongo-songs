import os
import pymongo

mongo_client = pymongo.MongoClient(
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
)

mongo_songs_db = mongo_client[os.getenv("MONGO_SONGS_DB_NAME")]
