from typing import Optional
from ninja import Schema
from pydantic import Field
from .models import MediaTypeChoices

class PersonIn(Schema):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    bio: Optional[str] = ""

class PersonOut(Schema):
    id: int
    first_name: str
    last_name: str
    bio: str

class StudioIn(Schema):
    name: str = Field(..., max_length=150)
    description: Optional[str] = ""

class StudioOut(Schema):
    id: int
    name: str
    description: str

class FilmMediaIn(Schema):
    media_type: MediaTypeChoices
    external_url: Optional[str] = None

class FilmMediaOut(Schema):
    id: int
    media_type: str
    file: Optional[str] = None
    external_url: Optional[str] = None

class UserOut(Schema):
    id: int
    username: str

class ReviewIn(Schema):
    text: str = Field(..., description="Текст рецензии")
    rating: int = Field(..., ge=1, le=10, description="Рейтинг от 1 до 10")

class ReviewOut(Schema):
    id: int
    text: str
    rating: int
    author: UserOut
    created_at: str

class FilmIn(Schema):
    title: str = Field(..., max_length=255)
    year: int = Field(..., gt=1800)
    description: Optional[str] = ""
    studio_id: Optional[int] = None
    director_ids: list[int] = []
    actor_ids: list[int] = []
    producer_ids: list[int] = []

class FilmOut(Schema):
    id: int
    title: str
    year: int
    description: str
    studio: Optional[StudioOut] = None
    directors: list[PersonOut]
    actors: list[PersonOut]
    producers: list[PersonOut]
    media_files: list[FilmMediaOut] = []
    reviews: list[ReviewOut] = []