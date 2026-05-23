from typing import Optional
from ninja import Schema  
from pydantic import Field

class AuthorIn(Schema):
    first_name: str = Field(..., max_length=100, description="Имя автора")
    last_name: str = Field(..., max_length=100, description="Фамилия автора")
    patronymic: Optional[str] = Field(None, max_length=100, description="Отчество автора (необязательно)")
    bio: Optional[str] = Field("", description="Биография")

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str]
    bio: str

class BookIn(Schema): 
    title: str = Field(..., max_length=255, description="Название книги")
    description: Optional[str] = Field("", description="Описание книги")
    publication_year: int = Field(..., gt=0, description="Год публикации")
    pages_count: int = Field(..., gt=0, description="Количество страниц")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг от 1 до 5")
    genre: str = Field(..., max_length=100, description="Жанр книги")
    author_id: int = Field(..., description="ID существующего автора")

class BookOut(Schema):
    id: int
    title: str
    description: str
    publication_year: int
    pages_count: int
    rating: int
    genre: str
    author: AuthorOut 