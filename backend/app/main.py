import os
from dotenv import load_dotenv

from typing import Union, Callable, Optional

from fastapi import FastAPI, Depends, Body, Response, HTTPException, status

from contextlib import asynccontextmanager

from app.models.comment import CommentModel, UpdateCommentModel, CommentCollection

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

def get_prod_db():
    return motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))

app = FastAPI(
    title="WebsiteCommentDatabase",
    description="A simple API to manage comments on a webpage through a chrome extension",
    version="0.1.0",
    openapi_tags=tags_metadata
)

# Define routes here or include routers
@app.get("/", tags=["Other"])
async def read_root():
    return {"Hello": "World"}

@app.post(
    "/comments/",
    response_description="Add new comment",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def create_comment(comment: CommentModel = Body(...), client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    Insert a new comment record.
    A unique `id` will be created and provided in the response.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    new_comment = await comment_collection.insert_one(
        comment.model_dump(by_alias=True, exclude=["id"])
    )
    created_comment = await comment_collection.find_one(
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
async def list_comments(client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    List all of the comment data in the database.
    The response is unpaginated and limited to 1000 results.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    return CommentCollection(comments=await comment_collection.find().to_list(1000))

@app.get(
    "/comments/{webpage}",
    response_description="Comments form specific website",
    response_model=CommentCollection,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def website_comments(webpage: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    List comments data in the database for the specific
    website the user is currently on.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    comments_for_site = await comment_collection.find({"webpage": webpage}).to_list(1000)
    return CommentCollection(comments=comments_for_site)

@app.get(
    "/comments/{id}",
    response_description="Get a comment by ID",
    response_model=CommentModel,
    response_model_by_alias=False,
    tags=["Comment Functions"]
)
async def get_comment(id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    Get a single comment from the database by ID.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    if (
        comment := await comment_collection.find_one({"_id": ObjectId(id)})
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
async def update_comment(id: str, comment: UpdateCommentModel = Body(...), client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    Update individual fields of an existing comment record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    comment = {
        k: v for k, v in comment.model_dump(by_alias=True).items() if v is not None
    }
    if len(comment) >= 1:
        update_result = await comment_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": comment},
            return_document=ReturnDocument.AFTER,
        )

        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Comment {id} not found!")

    # The update is empty, but we should still return the matching document:
    if (existing_comment := await comment_collection.find_one({"_id": id})) is not None:
        return existing_comment

    # Something went wrong
    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")

@app.delete(
    "/comments/{id}", 
    response_description="Delete a comment",
    tags=["Comment Functions"]
)
async def delete_comment(id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)):
    """
    Remove a single comment record from the database.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    delete_result = await comment_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")
