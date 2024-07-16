from fastapi import APIRouter
from .api import router as validation_router
from app.config import settings

router = APIRouter(
)

router.include_router(validation_router)
