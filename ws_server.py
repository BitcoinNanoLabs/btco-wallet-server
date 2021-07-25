import asyncio
import websockets
from logging import getLogger, INFO, StreamHandler

logger = getLogger('websockets')
logger.setLevel(INFO)
logger.addHandler(StreamHandler())

clients = set()

async def handler(websocket, path):
    msg = await websocket.recv()
    print(f"Received: {msg}")
    global clients
    clients.add(websocket)
    try:
        await asyncio.wait([ws.send("{\"ack\": \"subscribe\",\"time\": \"10\"}") for ws in clients])
        await asyncio.sleep(10)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, port=7078)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()