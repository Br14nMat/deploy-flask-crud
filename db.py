from pymongo import MongoClient
import os

#Los certificados TLS/SSL
import certifi

MONGO_URI = os.getenv("MONGODB_URI")
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["products"]
    except ConnectionError:
        print("Error de conexion con la bd")
    return db