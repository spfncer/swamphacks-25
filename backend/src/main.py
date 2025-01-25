import os
from dotenv import load_dotenv
from typing import Union

from fastapi import FastAPI

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(
    os.environ.get("MONGO_ATLAS_CONNECTION_STRING"), server_api=ServerApi("1")
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    # Send a ping to confirm a successful connection to Mongo
    try:
        client.admin.command("ping")
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
