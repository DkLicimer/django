from django.shortcuts import get_object_or_404
from ninja import Router
from django.contrib.auth import get_user_model
from config.auth import JWTAuth, JWTStaffAuth
from .models import Person, Studio, Film, Review
from .schemas import (
    PersonIn, PersonOut,
    StudioIn, StudioOut,
    FilmIn, FilmOut,
    ReviewIn, ReviewOut
)

router = Router()
User = get_user_model()

@router.post("/persons", response={201: PersonOut}, auth=JWTStaffAuth()) 
def create_person(request, payload: PersonIn):
    person = Person.objects.create(**payload.dict())
    return 201, person

@router.get("/persons", response=list[PersonOut]) 
def list_persons(request):
    return Person.objects.all()

@router.post("/studios", response={201: StudioOut}, auth=JWTStaffAuth())  
def create_studio(request, payload: StudioIn):
    studio = Studio.objects.create(**payload.dict())
    return 201, studio

@router.get("/studios", response=list[StudioOut])
def list_studios(request):
    return Studio.objects.all()

@router.post("/films", response={201: FilmOut}, auth=JWTStaffAuth())  
def create_film(request, payload: FilmIn):
    studio = None
    if payload.studio_id:
        studio = get_object_or_404(Studio, id=payload.studio_id)
        
    film = Film.objects.create(
        title=payload.title,
        year=payload.year,
        description=payload.description,
        studio=studio
    )
    
    if payload.director_ids:
        directors = Person.objects.filter(id__in=payload.director_ids)
        film.directors.set(directors)
        
    if payload.actor_ids:
        actors = Person.objects.filter(id__in=payload.actor_ids)
        film.actors.set(actors)
        
    if payload.producer_ids:
        producers = Person.objects.filter(id__in=payload.producer_ids)
        film.producers.set(producers)
        
    film.save()
    return 201, film

@router.get("/films", response=list[FilmOut])  
def list_films(request):
    return Film.objects.select_related("studio")\
                       .prefetch_related("directors", "actors", "producers", "media_files", "reviews__author")\
                       .all()

@router.post("/films/{film_id}/reviews", response={201: ReviewOut}, auth=JWTAuth())
def create_review(request, film_id: int, payload: ReviewIn):
    film = get_object_or_404(Film, id=film_id)
    user = request.auth
    review = Review.objects.create(
        film=film,
        author=user,  
        text=payload.text,
        rating=payload.rating
    )
    return 201, review