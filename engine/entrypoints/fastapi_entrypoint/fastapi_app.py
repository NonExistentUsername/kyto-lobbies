from fastapi import FastAPI


app = FastAPI()

# TODO: For first time, we will recieve uuid of player from client,
# but later we will use JWT and auth microservice


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
