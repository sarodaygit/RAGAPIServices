from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

# Support for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Awards(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None

class IMDb(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id: Optional[int] = None

class Viewer(BaseModel):
    rating: Optional[float] = None
    numReviews: Optional[int] = None
    meter: Optional[int] = None

class Tomatoes(BaseModel):
    viewer: Optional[Viewer] = None
    dvd: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None

class Movie(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    rated: Optional[str] = None
    cast: Optional[List[str]] = None
    num_mflix_comments: Optional[int] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None
    awards: Optional[Awards] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[IMDb] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[Tomatoes] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_objectid(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
