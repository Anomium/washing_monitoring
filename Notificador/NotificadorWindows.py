import asyncio

from .Notificador import Notificador

try:
    from winotify import Notification, audio
    WINOTIFY_OK = True
except ImportError:
    WINOTIFY_OK = False

class NotificadorWindows(Notificador):
    def __init__(self, app_id: str = "Monitor Lavadora") -> None:
        super().__init__()
        self.app_id = app_id
        if not WINOTIFY_OK:
            self.log.warning("winotify no está instalado; no habrá notificaciones de Windows.")
 
    def _mostrar(self, titulo: str, mensaje: str) -> None:
        toast = Notification(
            app_id=self.app_id,
            title=titulo,
            msg=mensaje,
            duration="long",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
 
    async def enviar(self, titulo: str, mensaje: str) -> None:
        if not WINOTIFY_OK:
            return
        try:
            await asyncio.to_thread(self._mostrar, titulo, mensaje)
            self.log.info("Notificación mostrada.")
        except Exception as e:
            self.log.error(f"No se pudo mostrar la notificación: {e}")