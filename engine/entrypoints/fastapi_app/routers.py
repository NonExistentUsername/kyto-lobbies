from entrypoints.fastapi_app.v1.routers import router as v1_router
from fastapi import APIRouter

"""
Here we will include all routers
"""

main_router = APIRouter(
    prefix="",
    tags=["main"],
)

main_router.include_router(v1_router)
