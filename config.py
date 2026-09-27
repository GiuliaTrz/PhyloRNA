from pymongo import MongoClient
import urllib.parse
import os
from dotenv import load_dotenv

# Connessione Atlas
uri = os.getenv("db_uri")

CLIENT = MongoClient(uri, tlsAllowInvalidCertificates=True)
DB = CLIENT[os.getenv("db_name")]
COLLECTION = DB[os.getenv("collection_name")]
