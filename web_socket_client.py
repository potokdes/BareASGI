import websockets
import asyncio


async def listen():
    url = "ws://127.0.0.1:8000"

    async with websockets.connect(url) as ws:
        while True:
            try:
                msg = await ws.recv()
                print(msg)
            except websockets.exceptions.ConnectionClosedOK as e:
                print(e)
                break


asyncio.get_event_loop().run_until_complete(listen())
