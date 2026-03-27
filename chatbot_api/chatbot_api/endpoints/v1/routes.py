'''
A router for all v1 endpoints
'''
from fastapi import APIRouter

from chatbot_api.endpoints.v1 import health, chatbot

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])