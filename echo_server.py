import asyncio
from websockets.asyncio.server import serve
import socket

async def print_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

async def echo(websocket):
    client_ip, client_port = websocket.remote_address
    print(f"🔌 Client connected from {client_ip}:{client_port}")

    async for message in websocket:
        await websocket.send(f"📦 Echo: {message}")

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        print("🚀 PDF - WebSocket connected!")
        print(f"🗺️ WebSocket IP address: ws://{await print_ip()}:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
