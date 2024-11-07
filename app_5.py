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


async def handle_http(scope: Scope, receive: Receive, send: Send):
    chunks = []
    while True:
        msg = await receive()
        if msg["type"] == "http.disconnect":
            return
        chunks.append(msg["body"])

        if not msg["more_body"]:
            break

    body = b"".join(chunks)
    print(body)

    response_start = {
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"Content-Type", b"application/json")],
    }
    await send(response_start)
    response_body = {
        "type": "http.response.body",
        "body": b"{'message':'body'}",
        "more_body": False,
    }
    await send(response_body)


async def handle_websocket(scope: Scope, receive: Receive, send: Send):
    msg = await receive()
    print(msg)
    response_start = {
        "type": "websocket.accept",
        "subprotocol": None,
        "headers": [],
    }
    await send(response_start)
    for i in range(1, 11):
        response_start = {
            "type": "websocket.send",
            "text": f"To jest widomość {i}/10",
        }
        await send(response_start)

    response_start = {
        "type": "websocket.close",
        "reason": f"Wyczerpano dane",
    }
    await send(response_start)
    msg = await receive()
    print(msg)


async def app(scope: Scope, receive: Receive, send: Send) -> App:
    print(scope)
    if scope["type"] == "lifespan":
        await handle_lifespan(scope, receive, send)
    elif scope["type"] == "http":
        await handle_http(scope, receive, send)
    elif scope["type"] == "websocket":
        await handle_websocket(scope, receive, send)
    else:
        pass


if __name__ == "__main__":
    uvicorn.run(app=app)
