from fastapi import APIRouter

api_v1_router = APIRouter(
    prefix="/v1",
    tags=["api_v1"],
    responses={404: {"description": "Not found"}},
)
