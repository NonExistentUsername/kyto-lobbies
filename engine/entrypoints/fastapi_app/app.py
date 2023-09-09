from fastapi import FastAPI

# TODO: For first time, we will recieve uuid of player from client,
# but later we will use JWT and auth microservice


def create_app() -> "FastAPI":
    from entrypoints.fastapi_app.routers import main_router

    app = FastAPI()
    app.include_router(main_router)

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
