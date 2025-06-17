# echo_server.py
import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        print("Please be patient. You are being hacked! 🚀")
        await asyncio.Future()  # run forever

asyncio.run(main())
