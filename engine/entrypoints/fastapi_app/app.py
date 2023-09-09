from fastapi import FastAPI

# TODO: For first time, we will recieve uuid of player from client,
# but later we will use JWT and auth microservice


def create_app() -> "FastAPI":
    from entrypoints.fastapi_app.routers import api_v1_router

    app = FastAPI()

    app.include_router(api_v1_router, prefix="/api/v1")

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
