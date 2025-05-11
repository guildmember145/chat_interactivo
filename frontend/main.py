#!/usr/bin/env python3
"""
Frontend para chat en tiempo real con Flet.
"""

import flet as ft
import asyncio
import websockets
import logging

logging.basicConfig(
    level=logging.INFO, format=("%(asctime)s - %(levelname)s - %(message)s")
)


class ChatApp:
    """Clase principal para la app de chat."""

    def __init__(self, page: ft.Page, loop: asyncio.AbstractEventLoop):
        self.page = page
        self.loop = loop
        self.page.title = "Chat en Tiempo Real"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.chat_display = ft.Column(expand=True, scroll="auto")
        self.new_message = ft.TextField(
            hint_text="Escribe un mensaje...", expand=True
            )
        self.new_message.on_submit = self.send_message
        self.send_button = ft.ElevatedButton(
            text="Enviar",
            on_click=self.send_message
        )
        self.websocket = None

        self.build_ui()

    async def connect_websocket(self):
        """Conecta al servidor WebSocket."""
        uri = "ws://localhost:8000/ws"
        try:
            self.websocket = await websockets.connect(uri)
            logging.info("Conexión WebSocket establecida.")
            await self.receive_messages()
        except ConnectionRefusedError:
            logging.error("Error: No se pudo conectar al servidor.")
            await self.display_message(
                "Error: No se pudo conectar al servidor."
                )
        except Exception as e:
            logging.error(f"Error al conectar al WS: {e}")
            await self.display_message(f"Error: {e}")

    async def display_message(self, message: str):
        """Muestra un mensaje en el chat."""
        self.chat_display.controls.append(ft.Text(message))
        self.page.update()

    def send_message(self, e):
        """Envía el mensaje del usuario."""
        self.loop.create_task(self._send_message_async())

    async def _send_message_async(self):
        """Envía mensajes de forma asíncrona."""
        if (
            self.websocket
            and self.websocket.close_code is None
            and self.new_message.value
        ):
            msg = self.new_message.value
            await self.websocket.send(msg)
            await self.display_message(f"Tú: {msg}")
            self.new_message.value = ""
            self.page.update()

    async def receive_messages(self):
        """Recibe mensajes del servidor."""
        if not self.websocket:
            return
        try:
            async for msg in self.websocket:
                await self.display_message(f"Otro: {msg}")
        except websockets.exceptions.ConnectionClosedError:
            logging.info("Conexión cerrada por el servidor.")
            await self.display_message("Conexión cerrada.")
        except Exception as e:
            logging.error(f"Error al recibir mensajes: {e}")
            await self.display_message(f"Error al recibir mensajes: {e}")
        finally:
            self.websocket = None
            self.page.update()

    def build_ui(self):
        """Construye la interfaz de usuario."""
        self.page.add(
            self.chat_display,
            ft.Row(
                [self.new_message, self.send_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )


async def main(page: ft.Page):
    """Inicia la app de chat."""
    loop = asyncio.get_running_loop()
    chat_app = ChatApp(page, loop)
    loop.create_task(chat_app.connect_websocket())


if __name__ == "__main__":
    ft.app(target=main)
