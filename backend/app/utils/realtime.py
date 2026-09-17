from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, email: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(email, []).append(websocket)

    def disconnect(self, email: str, websocket: WebSocket):
        sockets = self.connections.get(email, [])
        if websocket in sockets:
            sockets.remove(websocket)
        if not sockets:
            self.connections.pop(email, None)

    async def send(self, email: str, event: str, payload: dict):
        for socket in list(self.connections.get(email, [])):
            try:
                await socket.send_json({"event": event, "payload": payload})
            except Exception:
                self.disconnect(email, socket)


realtime = ConnectionManager()
