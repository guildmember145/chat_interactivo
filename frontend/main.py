#!/usr/bin/env python3
"""
Flet frontend for a real-time chat application.

This module defines the Flet application, including the UI layout,
WebSocket connection management, and message handling logic.
"""

import flet as ft
import asyncio
import websockets
import logging

logging.basicConfig(
    level=logging.INFO, format=("%(asctime)s - %(levelname)s - %(message)s")
)

WEBSOCKET_URI = "ws://localhost:8000/ws"


class ChatApp:
    """
    Main class for the Flet chat application.

    Manages the UI, WebSocket connection, and message sending/receiving.
    """

    def __init__(self, page: ft.Page, loop: asyncio.AbstractEventLoop):
        self.page = page
        self.loop = loop
        self.page.title = "Real-Time Chat"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.chat_display = ft.Column(expand=True, scroll="auto") # Area to display messages
        self.new_message = ft.TextField(
            hint_text="Type a message...", expand=True # Input field for new messages
            )
        self.new_message.on_submit = self.send_message # Send message on Enter key
        self.send_button = ft.ElevatedButton(
            text="Send",
            on_click=self.send_message # Send message on button click
        )
        self.websocket = None

        self.build_ui()

    async def connect_websocket(self):
        """
        Connects to the WebSocket server.

        Establishes a connection to the URI defined in WEBSOCKET_URI.
        If successful, starts listening for incoming messages.
        Handles connection errors and displays them to the user.
        """
        uri = WEBSOCKET_URI
        try:
            self.websocket = await websockets.connect(uri)
            logging.info("WebSocket connection established.")
            await self.display_message("Connected to the chat server.")
            await self.receive_messages()
        except ConnectionRefusedError:
            logging.error("Error: Could not connect to the server.")
            await self.display_message(
                "Error: Could not connect to the server. Please ensure the backend is running."
                )
        except Exception as e:
            logging.error(f"Error connecting to WebSocket: {e}")
            await self.display_message(f"Error connecting: {e}")

    async def display_message(self, message: str):
        """
        Displays a message in the chat UI.

        Appends the given message to the chat_display area and updates the page.
        """
        self.chat_display.controls.append(ft.Text(message))
        self.page.update()

    def send_message(self, e):
        """
        Handles the send message event (e.g., button click or Enter key).

        Creates an asyncio task to send the message asynchronously.
        """
        self.loop.create_task(self._send_message_async())

    async def _send_message_async(self):
        """
        Sends the user's message asynchronously over the WebSocket.

        Checks if the WebSocket connection is active and the message input is not empty.
        Sends the message, displays it locally as "You: <message>", and clears the input field.
        """
        if (
            self.websocket
            and self.websocket.close_code is None
            and self.new_message.value
        ):
            msg = self.new_message.value
            await self.websocket.send(msg)
            await self.display_message(f"You: {msg}")
            self.new_message.value = ""
            self.page.update()

    async def receive_messages(self):
        """
        Listens for and processes incoming messages from the WebSocket server.

        Iterates over messages received from the WebSocket. Displays messages from others.
        Handles server-initiated connection closure and other reception errors.
        """
        if not self.websocket:
            return
        try:
            async for msg in self.websocket:
                await self.display_message(f"Other: {msg}")
        except websockets.exceptions.ConnectionClosedError:
            logging.info("Connection closed by the server.")
            await self.display_message("Connection closed by the server.")
        except Exception as e:
            logging.error(f"Error receiving messages: {e}")
            await self.display_message(f"Error receiving messages: {e}")
        finally:
            self.websocket = None # Ensure websocket is None if connection is closed
            await self.display_message("Disconnected from chat.")
            self.page.update()

    def build_ui(self):
        """
        Constructs the Flet user interface.

        Adds the chat display area and the message input row (text field and send button)
        to the page.
        """
        self.page.add(
            self.chat_display,
            ft.Row(
                [self.new_message, self.send_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )


async def main(page: ft.Page):
    """
    Main entry point for the Flet application.

    Initializes the ChatApp and schedules the WebSocket connection.
    """
    loop = asyncio.get_running_loop()
    chat_app = ChatApp(page, loop)
    loop.create_task(chat_app.connect_websocket())


if __name__ == "__main__":
    ft.app(target=main)
