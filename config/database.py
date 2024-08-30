from bson import ObjectId
from pymongo import MongoClient

import urllib.parse

from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
database_name = os.getenv('MONGO_DATABASE_NAME')

uri = f"mongodb+srv://{username}:{password}@cluster0.octwf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, tls=True)
                     

db_client = client.channel

db = db_client[database_name]

def get_db():
    return db