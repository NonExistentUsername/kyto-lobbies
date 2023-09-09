from entrypoints.fastapi_app.v1.router import router as v1_router
from fastapi import APIRouter

main_router = APIRouter()
main_router.include_router(v1_router)
