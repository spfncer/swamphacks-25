from datetime import datetime
from typing import Optional, List
from typing_extensions import Annotated

from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class CommentModel(BaseModel):
    """
    Represents a comment for our extension on the webpage.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    webpage: str = Field(...)
    author: str = Field(...)
    body: str = Field(...)

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    def save(self):
        self.updated_at = datetime.utcnow()

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "webpage": "www.example.com",
                "author": "jdoe@example.com",
                "body": "This webpage seems relatively accurate based on my experience."
            }
        },
    )

class CommentCollection(BaseModel):
    """
    A container holding a list of `CommentModel` instances.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    comments: List[CommentModel]

class UpdateCommentModel(BaseModel):
    """
    A set of optional updates to be made to a comment in the database.
    """
    webpage: Optional[str] = None
    author: Optional[str] = None
    body: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "webpage": "www.example.com",
                "author": "jdoe@example.com",
                "body": "This webpage seems relatively accurate based on my experience."
            }
        },
    )