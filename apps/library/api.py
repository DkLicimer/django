from django.shortcuts import get_object_or_404
from ninja import Router, Query, File
from ninja.files import UploadedFile
from ninja.pagination import paginate, PageNumberPagination
from config.auth import JWTStaffAuth
from .models import Author, Book
from .schemas import AuthorIn, AuthorOut, BookIn, BookOut, BookFilterSchema

router = Router()

@router.post("/authors", response={201: AuthorOut}, auth=JWTStaffAuth())  # Защищен
def create_author(request, payload: AuthorIn):
    author = Author.objects.create(**payload.dict())
    return 201, author

@router.get("/authors", response=list[AuthorOut])  # Публичный
def list_authors(request):
    return Author.objects.all()

@router.get("/authors/{author_id}", response=AuthorOut)  # Публичный
def get_author(request, author_id: int):
    return get_object_or_404(Author, id=author_id)

@router.put("/authors/{author_id}", response=AuthorOut, auth=JWTStaffAuth())  # Защищен
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return author

@router.delete("/authors/{author_id}", response={204: None}, auth=JWTStaffAuth())  # Защищен
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return 204, None

@router.post("/books", response={201: BookOut}, auth=JWTStaffAuth())  # Защищен
def create_book(request, payload: BookIn):
    author = get_object_or_404(Author, id=payload.author_id)
    data = payload.dict()
    data.pop("author_id")
    book = Book.objects.create(author=author, **data)
    return 201, book

@router.get("/books", response=list[BookOut])  # Публичный
@paginate(PageNumberPagination, page_size=5)
def list_books(request, filters: BookFilterSchema = Query(...)):
    books = Book.objects.select_related("author").all()
    books = filters.filter(books)
    return books

@router.get("/books/{book_id}", response=BookOut)  # Публичный
def get_book(request, book_id: int):
    return get_object_or_404(Book.objects.select_related("author"), id=book_id)

@router.put("/books/{book_id}", response=BookOut, auth=JWTStaffAuth())  # Защищен
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    author = get_object_or_404(Author, id=payload.author_id)
    
    data = payload.dict()
    data.pop("author_id")
    
    for attr, value in data.items():
        setattr(book, attr, value)
    book.author = author
    book.save()
    return book

@router.delete("/books/{book_id}", response={204: None}, auth=JWTStaffAuth())  # Защищен
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return 204, None

@router.post("/books/{book_id}/cover", response=BookOut, auth=JWTStaffAuth())  # Защищен
def upload_book_cover(request, book_id: int, file: File[UploadedFile]):
    book = get_object_or_404(Book, id=book_id)
    if book.cover:
        book.cover.delete(save=False)
    book.cover = file
    book.save()
    return book