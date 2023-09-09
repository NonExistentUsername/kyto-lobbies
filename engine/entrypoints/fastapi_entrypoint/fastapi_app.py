from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from engine.entrypoints.fastapi_entrypoint.deps import get_current_user


app = FastAPI()

# TODO: For first time, we will recieve uuid of player from client,
# but later we will use JWT and auth microservice


@app.get("/")
async def root(uuid: Annotated[str, Depends(get_current_user)]) -> dict:
    return {"message": f"Hello {uuid}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
