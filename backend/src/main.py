import os
from dotenv import load_dotenv

from typing import Union

from fastapi import FastAPI, Body, Response, HTTPException, status

from models.comment import CommentModel, UpdateCommentModel, CommentCollection
from bson import ObjectId

import motor.motor_asyncio
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi

load_dotenv(dotenv_path="../.env")

tags_metadata = [
    {
        "name": "Comment Functions",
        "description": "Operations related to comments on a webpage.",
    },
    {
        "name": "Other"
    }
]

async def db_lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    app.database = app.mongodb_client.get_database("Comments")
    app.comment_collection = app.database.get_collection("websites")

    # Try pinging the database to ensure connection
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()

app = FastAPI(
    title="WebsiteCommentDatabase",
    description="A simple API to manage comments on a webpage through a chrome extension",
    version="0.1.0",
    openapi_tags=tags_metadata,
    lifespan=db_lifespan
)

# Other

@app.get("/", tags=["Other"])
async def read_root():
    return {"Hello": "World"}

# Comments

@app.post(
    "/comments/",
    response_description="Add new comment",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def create_comment(comment: CommentModel = Body(...)):
    """
    Insert a new comment record.
    A unique `id` will be created and provided in the response.
    """
    new_comment = await app.comment_collection.insert_one(
        comment.model_dump(by_alias=True, exclude=["id"])
    )
    created_comment = await app.comment_collection.find_one(
        {"_id": new_comment.inserted_id}
    )
    return created_comment

@app.get(
    "/comments/",
    response_description="List all comments",
    response_model=CommentCollection,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def list_comments():
    """
    List all of the comment data in the database.
    The response is unpaginated and limited to 1000 results.
    """
    return CommentCollection(comments=await app.comment_collection.find().to_list(1000))

@app.get(
    "/comments/{id}",
    response_description="Get a comment by ID",
    response_model=CommentModel,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def get_comment(id: str):
    """
    Get a single comment from the database by ID.
    """
    if (
        comment := await app.comment_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return comment
    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")

@app.put(
    "/comments/{id}",
    response_description="Update a comment",
    response_model=CommentModel,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def update_comment(id: str, comment: UpdateCommentModel = Body(...)):
    """
    Update individual fields of an existing comment record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    comment = {
        k: v for k, v in comment.model_dump(by_alias=True).items() if v is not None
    }

    if len(comment) >= 1:
        update_result = await app.comment_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": comment},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Comment {id} not found!")

    # The update is empty, but we should still return the matching document:
    if (existing_comment := await app.comment_collection.find_one({"_id": id})) is not None:
        return existing_comment
    
    # Something went wrong
    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")

@app.delete(
    "/comments/{id}", 
    response_description="Delete a comment",
    tags=["Comment Functions"]
)
async def delete_comment(id: str):
    """
    Remove a single comment record from the database.
    """
    delete_result = await app.comment_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")
