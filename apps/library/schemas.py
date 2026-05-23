from typing import Annotated, Optional
from ninja import Schema, FilterSchema, FilterLookup  
from pydantic import Field
from .models import GenreChoices

class AuthorIn(Schema):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = ""

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str]
    bio: str

class BookIn(Schema):
    title: str = Field(..., max_length=255)
    description: Optional[str] = ""
    publication_year: int = Field(..., gt=0)
    pages_count: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    genre: GenreChoices = Field(..., description="Выбор жанра из доступных вариантов")  
    author_id: int

class BookOut(Schema):
    id: int
    title: str
    description: str
    publication_year: int
    pages_count: int
    rating: int
    genre: str
    cover: Optional[str] = None 
    author: AuthorOut

class BookFilterSchema(FilterSchema):
    title: Annotated[Optional[str], FilterLookup("title__icontains")] = None
    
    pub_year_from: Annotated[Optional[int], FilterLookup("publication_year__gte")] = None
    pub_year_to: Annotated[Optional[int], FilterLookup("publication_year__lte")] = None
    author_name: Annotated[
        Optional[str], 
        FilterLookup([
            "author__first_name__icontains", 
            "author__last_name__icontains", 
            "author__patronymic__icontains"
        ])
    ] = None
    
    author_id: Annotated[Optional[int], FilterLookup("author_id")] = None
    genre: Annotated[Optional[list[GenreChoices]], FilterLookup("genre__in")] = None
    pages_from: Annotated[Optional[int], FilterLookup("pages_count__gte")] = None
    pages_to: Annotated[Optional[int], FilterLookup("pages_count__lte")] = None
    rating: Annotated[Optional[int], FilterLookup("rating__gte")] = None