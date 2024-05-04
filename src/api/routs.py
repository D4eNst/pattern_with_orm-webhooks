from fastapi import APIRouter
from api.endpoints.webhooks import router as webhooks_router

router = APIRouter()

router.include_router(webhooks_router)
