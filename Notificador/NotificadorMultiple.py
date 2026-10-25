import asyncio

from .Notificador import Notificador

class NotificadorMultiple(Notificador):
    """Envía el mismo aviso por varios canales en paralelo."""
 
    def __init__(self, *canales: Notificador) -> None:
        super().__init__()
        self.canales = list(canales)
 
    async def enviar(self, titulo: str, mensaje: str) -> None:
        await asyncio.gather(*(c.enviar(titulo, mensaje) for c in self.canales))
 
    async def cerrar(self) -> None:
        await asyncio.gather(*(c.cerrar() for c in self.canales))