import logging
from abc import ABC, abstractmethod

class Notificador(ABC):
    """Interfaz común para cualquier canal de notificación."""
 
    def __init__(self) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
 
    @abstractmethod
    async def enviar(self, titulo: str, mensaje: str) -> None:
        ...
 
    async def cerrar(self) -> None:
        """Libera recursos si el canal los usa."""