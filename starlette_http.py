    async def stream(self) -> typing.AsyncGenerator[bytes, None]:
        if hasattr(self, "_body"):
            yield self._body
            yield b""
            return
        if self._stream_consumed:
            raise RuntimeError("Stream consumed")
        while not self._stream_consumed:
            message = await self._receive()
            if message["type"] == "http.request":
                body = message.get("body", b"")
                if not message.get("more_body", False):
                    self._stream_consumed = True
                if body:
                    yield body
            elif message["type"] == "http.disconnect":
                self._is_disconnected = True
                raise ClientDisconnect()
        yield b""

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        prefix = "websocket." if scope["type"] == "websocket" else ""
        await send(
            {
                "type": prefix + "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        await send({"type": prefix + "http.response.body", "body": self.body})

        if self.background is not None:
            await self.background()