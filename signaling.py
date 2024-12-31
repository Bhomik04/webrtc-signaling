from aiohttp import web
import asyncio
import json

clients = {}

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    user_id = request.match_info['user_id']
    clients[user_id] = ws
    print(f"[INFO] Client {user_id} connected.")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                target_user_id, data = msg.data.split(":", 1)
                if target_user_id in clients:
                    await clients[target_user_id].send_str(data)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"[ERROR] WebSocket error: {ws.exception()}")
    finally:
        del clients[user_id]
        print(f"[INFO] Client {user_id} disconnected.")
    return ws

app = web.Application()
app.router.add_get('/ws/{user_id}', websocket_handler)

if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0",port=8080)