#!/usr/bin/env python3
"""
Backend para chat en tiempo real con FastAPI
y WebSockets.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    level=logging.INFO, format=("%(asctime)s - %(levelname)s - %(message)s")
)

app = FastAPI(
    title="Realtime Chat Backend",
    description=(
        "Backend para chat en tiempo real con "
        "FastAPI y WebSockets."
        ),
    version="0.1.0",
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

PRODUCTION_ORIGINS = ["https://example.com", "https://anotherdomain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=PRODUCTION_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint para manejar el chat via WebSocket."""
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
        logging.info("Cliente desconectado.")
    except Exception as err:
        logging.error(f"Error en WebSocket: {err}")
        clients.remove(websocket)
