from entrypoints.fastapi_app.responses import Response
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


def rewrite_404_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content=Response(
            message="Not found",
            status_code=404,
            success=False,
        ).model_dump(),
    )
