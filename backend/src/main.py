from typing import Union

from fastapi import FastAPI, Body, status

from models.comment import CommentModel, UpdateCommentModel, CommentCollection

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Upload comment

@app.post(
    "/comments/",
    response_description="Add new comment",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_comment(student: CommentModel = Body(...)):
    """
    Insert a new comment record.
    A unique `id` will be created and provided in the response.
    """
    raise HTTPException(status_code=501, detail=f"Not Implemented")


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
    raise HTTPException(status_code=501, detail=f"Not Implemented")

@app.get(
    "/comments/{id}",
    response_description="Get a comment by ID",
    response_model=CommentCollection,
    response_model_by_alias=False,
)
async def get_comment(id: str):
    """
    Get a single comment from the database by ID.
    """
    # TODO: get comment
    raise HTTPException(status_code=501, detail=f"Not Implemented")

@app.put(
    "/comments/{id}",
    response_description="Update a comment",
    response_model=CommentModel,
    response_model_by_alias=False,
)
async def update_comment(id: str, comment: UpdateCommentModel = Body(...)):
    """
    Update individual fields of an existing student record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    comment = {
        k: v for k, v in comment.model_dump(by_alias=True).items() if v is not None
    }

    # if len(comment) >= 1:
        #Perform Update
        # If update results isn't none then return
        # otherwise raise http exception 404

    # The update is empty, but we should still return the matching document:
    # if (existing_comment := await comment_collection.find_one({"_id": id})) is not None:
    #     return existing_comment
    
    # Something went wrong
    raise HTTPException(status_code=501, detail=f"Not Implemented")


@app.delete(
    "/comments/{id}", 
    response_description="Delete a student"
)
async def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    raise HTTPException(status_code=501, detail=f"Not Implemented")

