import os
from dotenv import load_dotenv

from typing import Union, Callable, Optional

from fastapi import FastAPI, Depends, Body, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.models.comment import (
    CommentModel,
    UpdateCommentModel,
    CommentCollection,
    CommentFilters,
)

from bson import ObjectId

import motor.motor_asyncio
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi

from starlette.middleware.sessions import SessionMiddleware  # 👈 new code
from auth.routes import auth_router  # 👈 new code

# Added for login success page
from fastapi.staticfiles import StaticFiles


load_dotenv(dotenv_path="../.env")

tags_metadata = [
    {
        "name": "Comment Functions",
        "description": "Operations related to comments on a webpage.",
    },
    {
        "name": "Authentication Functions",
        "description": "Operations related to authentication with Auth0.",
    },
    {"name": "Other"},
]


def get_prod_db():
    return motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))


app = FastAPI(
    title="WebsiteCommentDatabase",
    description="A simple API to manage comments on a webpage through a chrome extension",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("APP_SECRET_KEY"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)


# Define routes here or include routers
@app.get("/", tags=["Other"])
async def read_root():
    return {"Hello": "World"}

@app.post(
    "/comments",
    response_description="Add new comment",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    tags=["Comment Functions"],
)
async def create_comment(
    comment: CommentModel = Body(...),
    client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db),
):
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


@app.post(
    "/comments/search",
    response_description="Search for comments based on given filters",
    response_model=CommentCollection,
    response_model_by_alias=False,
    tags=["Comment Functions"],
)
async def search_comments(
    filters: CommentFilters,
    client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db),
):
    """
    List comments data in the database based on user provided search queries.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    query = {}

    if filters.ids:
        query["_id"] = {"$in": [str(id) for id in filters.ids]}

    if filters.webpage:
        query["webpage"] = filters.webpage

    if filters.author:
        query["author"] = filters.author

    if filters.body:
        query["body"] = {
            "$regex": filters.body,
            "$options": "i",
        }  # Case-insensitive search for body

    result_comments = await comment_collection.find(query).to_list(1000)
    return CommentCollection(comments=result_comments)


@app.get(
    "/comments/{id}",
    response_description="Get a comment by ID",
    response_model=CommentModel,
    response_model_by_alias=False,
    tags=["Comment Functions"],
)
async def get_comment(
    id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)
):
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
    tags=["Comment Functions"],
)
async def update_comment(
    id: str,
    comment: UpdateCommentModel = Body(...),
    client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db),
):
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
    tags=["Comment Functions"],
)
async def delete_comment(
    id: str, client: motor.motor_asyncio.AsyncIOMotorClient = Depends(get_prod_db)
):
    """
    Remove a single comment record from the database.
    """
    db = client["Comments"]
    comment_collection = db["websites"]

    delete_result = await comment_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Comment {id} not found!")
