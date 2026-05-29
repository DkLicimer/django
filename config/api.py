from ninja import NinjaAPI, Router, Schema
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from config.auth import generate_token
from apps.library.api import router as library_router
from apps.movies.api import router as movies_router

api = NinjaAPI(
    title="Secure Library & Cinema API",
    version="1.0.0",
    description="Учебный проект API"
)

auth_router = Router()

class LoginIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str

@auth_router.post("/token", response=TokenOut)
def get_token(request, payload: LoginIn):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Неверное имя пользователя или пароль")
    
    token = generate_token(user)
    return {"access_token": token}

api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/library", library_router, tags=["Books"])
api.add_router("/cinema", movies_router, tags=["Movies"])