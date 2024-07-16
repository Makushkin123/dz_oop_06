import hashlib
import datetime
import random
from fastapi.responses import JSONResponse
from app.shemas.score import MethodRequest
from app.config import settings


def check_users(request: MethodRequest):
    if not check_auth(request):
        return JSONResponse(
            status_code=403,
            content={"code": 403, "error": "Forbidden", "has": request.get_empty_fields()}
        )
    return request


def check_auth(request: MethodRequest):
    if request.is_admin:
        digest = hashlib.sha512(
            (datetime.datetime.now().strftime("%Y%m%d%H") + settings.ADMIN_SALT).encode('utf-8')).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + settings.SALT).encode('utf-8')).hexdigest()
    return digest == request.token


def get_score(phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    score = 0
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    return score


def get_interests():
    interests = ["cars", "pets", "travel", "hi-tech", "sport", "music", "books", "tv", "cinema", "geek", "otus"]
    return random.sample(interests, 2)
