from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pika
import json
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

class QueueMessage(BaseModel):
    payload: str

# 1. The Producer Endpoint (Frontend -> Broker)
@app.post("/produce")
async def produce_message(msg: QueueMessage):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='assignment_1_queue', durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key='assignment_1_queue',
        body=json.dumps({"message": msg.payload}),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
    )
    connection.close()
    return {"status": "success"}

# 2. The Internal Webhook Endpoint (Consumer -> FastAPI Server)
@app.post("/notify-frontend")
async def notify_frontend(msg: QueueMessage):
    """Consumer hits this endpoint when a job is done to trigger the WebSocket."""
    await manager.broadcast({"message": msg.payload})
    return {"status": "broadcasted"}

# 3. The WebSocket Endpoint (FastAPI Server <-> Browser)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keeps connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)