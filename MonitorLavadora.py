from __future__ import annotations

import asyncio
import logging
import time

from Configuracion  import Configuracion 
from DetectorCiclo import DetectorCiclo
from EnchufeKasa import EnchufeKasa
from Notificador import (Notificador, NotificadorAlexa, NotificadorMultiple, NotificadorWindows)


class MonitorLavadora:
    def __init__(self, config: Configuracion, enchufe: EnchufeKasa,
                 detector: DetectorCiclo, notificador: Notificador) -> None:
        self.config = config
        self.enchufe = enchufe
        self.detector = detector
        self.notificador = notificador
        self.log = logging.getLogger("MonitorLavadora")
        self._revision_inicial_pendiente = True
 
    @classmethod
    def desde_configuracion(cls, config: Configuracion) -> "MonitorLavadora":
        """Construye el monitor con todos sus componentes."""
        canales: list[Notificador] = [NotificadorWindows()]
        if config.alexa_token and config.alexa_dispositivo:
            canales.append(NotificadorAlexa(config.alexa_token, config.alexa_dispositivo))
        return cls(
            config=config,
            enchufe=EnchufeKasa(config.ip, config.usuario, config.clave),
            detector=DetectorCiclo(
                config.umbral_encendido_w,
                config.umbral_terminado_w,
                config.tiempo_espera_s,
            ),
            notificador=NotificadorMultiple(*canales),
        )
 
    async def ejecutar(self) -> None:
        await self.notificador.enviar("Lavadora", "✅ El programa de la lavadora ha sido iniciado.")
        try:
            while True:
                await self._ciclo()
        finally:
            await self.enchufe.desconectar()
            await self.notificador.cerrar()
 
    async def _ciclo(self) -> None:
        try:
            watts = await self.enchufe.leer_watts()
        except Exception as e:
            self.log.warning(f"Error con el enchufe: {e}. Reintento en {self.config.reintento_s:.0f} s.")
            await self.enchufe.desconectar()
            await asyncio.sleep(self.config.reintento_s)
            return
 
        if self._revision_inicial_pendiente:
            self._revision_inicial_pendiente = False
            await self._revisar_estado_inicial(watts)
 
        duracion = self.detector.procesar(watts, time.monotonic())
        if duracion is not None:
            await self.notificador.enviar(
                "Lavadora",
                f"🧺 La lavadora terminó. Duración aproximada: {duracion:.0f} min.",
            )
 
        await asyncio.sleep(self.config.intervalo_s)
 
    async def _revisar_estado_inicial(self, watts: float) -> None:
        """Solo con la primera lectura: avisa si la lavadora está prendida pero sin ciclo."""
        if self.config.umbral_prendida_w < watts <= self.config.umbral_encendido_w:
            self.log.info(f"Lavadora prendida sin ciclo al iniciar ({watts:.1f} W).")
            await self.notificador.enviar(
                "Lavadora",
                f"⚠️ La lavadora está prendida pero no ha iniciado ({watts:.1f} W).",
            )
