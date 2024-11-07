from collections.abc import MutableMapping, Callable, Awaitable
from typing import Any

import uvicorn

type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]
type App = Callable[[Scope, Receive, Send], Awaitable[None]]


async def app(scope: Scope, receive: Receive, send: Send) -> App:
    print(scope)
    msg = await receive()
    print(msg)


if __name__ == "__main__":
    uvicorn.run(app=app)


# {
#     "type": "lifespan",
#     "asgi": {"version": "3.0", "spec_version": "2.0"},
#     "state": {},
# }
# {"type": "lifespan.startup"}
