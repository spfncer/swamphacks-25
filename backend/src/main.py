from typing import Union

from fastapi import FastAPI

from models.comment import CommentCollection

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Upload comment

@app.get(
    "/comments/",
    response_description="List all comments",
    response_model=CommentCollection,
    response_model_by_alias=False,
)
async def list_comments():
    """
    List all of the comment data in the database.
    The response is unpaginated and limited to 1000 results.
    """
    return CommentCollection(comments=[])
    # return CommentCollection(comments=await student_collection.find().to_list(1000))

