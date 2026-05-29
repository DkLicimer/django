import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import jwt
from ninja.security import HttpBearer

User = get_user_model()

class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return None
            return User.objects.get(id=user_id)
        except (jwt.PyJWTError, User.DoesNotExist):
            return None

class JWTStaffAuth(JWTAuth):
    def authenticate(self, request, token: str):
        user = super().authenticate(request, token)
        if user and user.is_staff:
            return user
        return None

def generate_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "exp": timezone.now() + datetime.timedelta(days=1),
        "iat": timezone.now(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")