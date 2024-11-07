import uvicorn


async def app(scope, receive, send):
    pass


if __name__ == "__main__":
    uvicorn.run(app=app)
