import asyncio
from websockets.asyncio.server import serve
import socket

async def print_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable—just used to determine the outbound interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

async def echo(websocket):
    client_ip, client_port = websocket.remote_address
    print(f"🔌 Client connected from {client_ip}:{client_port}")

    async for message in websocket:
        print(f"📥 Message received: {message}")
        await websocket.send(f"📦 Echo: {message}")

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        print("🚀 PDF - WebSocket connected!")
        print(f"🗺️ WebSocket IP address: ws://{await print_ip()}:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
