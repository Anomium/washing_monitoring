from __future__ import annotations

import re
from typing import Optional

import aiohttp

from .Notificador import Notificador


class NotificadorAlexa(Notificador):
    """Hace que un Echo anuncie el mensaje en voz alta usando el skill Voice Monkey."""

    URL = "https://api-v3.voicemonkey.io/announce"

    def __init__(self, token: str, dispositivo: str) -> None:
        super().__init__()
        self.token = token
        self.dispositivo = dispositivo
        self._sesion: Optional[aiohttp.ClientSession] = None

    async def _obtener_sesion(self) -> aiohttp.ClientSession:
        if self._sesion is None or self._sesion.closed:
            self._sesion = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._sesion

    @staticmethod
    def _limpiar(texto: str) -> str:
        """Quita emojis y símbolos que Alexa no sabe leer."""
        return re.sub(r"[^\w\s.,;:¡!¿?()%-]", "", texto).strip()

    async def enviar(self, titulo: str, mensaje: str) -> None:
        params = {
            "token": self.token,
            "device": self.dispositivo,
            "speech": f"{self._limpiar(titulo)}. {self._limpiar(mensaje)}",
            "language": "es-US",
        }
        try:
            sesion = await self._obtener_sesion()
            async with sesion.get(self.URL, params=params) as r:
                body = await r.text()
                if r.status == 200:
                    self.log.info("Anuncio enviado a Alexa.")
                else:
                    self.log.error(f"Voice Monkey respondió {r.status}: {cuerpo[:200]}")
        except Exception as e:
            self.log.error(f"No se pudo enviar el anuncio a Alexa: {e}")

    async def cerrar(self) -> None:
        if self._sesion is not None and not self._sesion.closed:
            await self._sesion.close()
