from __future__ import annotations

import logging
from typing import Optional

from kasa import (
    Credentials,
    Device,
    DeviceConfig,
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
    Discover,
    Module,
)

class EnchufeKasa:
    """Maneja la conexión con el EP25 y la lectura de consumo."""
 
    def __init__(self, ip: str, usuario: str, clave: str) -> None:
        self.ip = ip
        self.credenciales = Credentials(usuario, clave)
        self._dev: Optional[Device] = None
        self._energia = None
        self.log = logging.getLogger("EnchufeKasa")
 
    @property
    def conectado(self) -> bool:
        return self._dev is not None
 
    async def conectar(self) -> None:
        dev = await self._descubrir() or await self._conectar_directo()
        energia = dev.modules.get(Module.Energy)
        if energia is None:
            await dev.disconnect()
            raise RuntimeError("El dispositivo no reporta consumo de energía.")
        self._dev, self._energia = dev, energia
        self.log.info(f"Conectado a {dev.alias} ({dev.model})")
 
    async def _descubrir(self) -> Optional[Device]:
        try:
            dev = await Discover.discover_single(
                self.ip, credentials=self.credenciales, discovery_timeout=5
            )
            await dev.update()
            return dev
        except Exception as e:
            self.log.info(f"Descubrimiento falló ({e}). Probando conexión directa KLAP...")
            return None
 
    async def _conectar_directo(self) -> Device:
        config = DeviceConfig(
            host=self.ip,
            credentials=self.credenciales,
            connection_type=DeviceConnectionParameters(
                device_family=DeviceFamily.IotSmartPlugSwitch,
                encryption_type=DeviceEncryptionType.Klap,
                login_version=2,
            ),
        )
        return await Device.connect(config=config)
 
    async def leer_watts(self) -> float:
        """Devuelve el consumo actual en vatios. Conecta si hace falta."""
        if not self.conectado:
            await self.conectar()
        await self._dev.update()
        return self._energia.current_consumption or 0.0
 
    async def desconectar(self) -> None:
        if self._dev is not None:
            try:
                await self._dev.disconnect()
            except Exception:
                pass
        self._dev = None
        self._energia = None