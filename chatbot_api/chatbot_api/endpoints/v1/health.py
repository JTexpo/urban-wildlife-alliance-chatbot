"""
A health endpoint using fastapi router
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health():
    """
    Return a health status of the application.

    Returns:
        dict: A dictionary containing a single key-value pair {"status": "ok"}
    """
    return {"status": "ok"}


@router.get("/auth")
async def health():
    """
    Return a health status of the application.

    Returns:
        dict: A dictionary containing a single key-value pair {"status": "ok"}
    """
    return {"status": "ok"}
