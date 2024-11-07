import json
from collections.abc import MutableMapping, Callable, Awaitable
from typing import Any

import uvicorn


type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]
type App = Callable[[Scope, Receive, Send], Awaitable[None]]


async def handle_lifespan(scope: Scope, receive: Receive, send: Send):
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                print("Do some startup here!")
                await send({"type": "lifespan.startup.complete"})
            except BaseException:
                print("Startup Error")
                await send({"type": "lifespan.startup.failed"})
                break
        elif message["type"] == "lifespan.shutdown":

            try:
                print("Do some shutdown here!")
                await send({"type": "lifespan.shutdown.complete"})
            except BaseException:
                await send({"type": "lifespan.shutdown.failed"})
            return


async def app(scope: Scope, receive: Receive, send: Send) -> App:
    if scope["type"] == "lifespan":
        await handle_lifespan(scope, receive, send)
    elif scope["type"] == "http":
        pass
    else:
        pass


if __name__ == "__main__":
    uvicorn.run(app=app)
