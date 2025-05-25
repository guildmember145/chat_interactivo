#!/usr/bin/env python3
"""
FastAPI backend for a real-time chat application using WebSockets.

This module sets up a FastAPI application with a WebSocket endpoint
for real-time communication between chat clients.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    level=logging.INFO, format=("%(asctime)s - %(levelname)s - %(message)s")
)

app = FastAPI(
    title="Real-Time Chat Backend",
    description="A FastAPI application that serves as the backend for a real-time chat using WebSockets.",
    version="0.1.0",
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Allow all origins for local development. This should be more restrictive in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for chat.

    Accepts a WebSocket connection, adds the client to the set of active clients,
    and then listens for incoming messages. When a message is received, it is
    broadcasted to all other connected clients. Handles client disconnection.
    """
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
        logging.info("Client disconnected.")
    except Exception as err:
        logging.error(f"Error in WebSocket connection: {err}")
        # Ensure client is removed on unexpected error
        if websocket in clients:
            clients.remove(websocket)
