from fastapi import FastAPI

# TODO: For first time, we will recieve uuid of player from client,
# but later we will use JWT and auth microservice


def create_app() -> "FastAPI":
    """
    Create FastAPI app
    Application will be created with all routers and exception handlers

    Returns:
        FastAPI: FastAPI app
    """
    from entrypoints.fastapi_app.exception_handlers import rewrite_404_exception
    from entrypoints.fastapi_app.v1.routers import router as api_v1_router

    app = FastAPI()
    app.include_router(api_v1_router)

    app.add_exception_handler(404, rewrite_404_exception)

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
