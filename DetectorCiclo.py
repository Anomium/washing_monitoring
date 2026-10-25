from __future__ import annotations

import logging
from typing import Optional


class DetectorCiclo:
    """
    Máquina de estados sin dependencias externas:
      - EN ESPERA: aguarda que el consumo supere el umbral de encendido.
      - LAVANDO:   aguarda que el consumo se mantenga bajo el tiempo indicado.
    """

    def __init__(self, umbral_encendido_w: float, umbral_terminado_w: float,
                 tiempo_espera_s: float) -> None:
        self.umbral_encendido_w = umbral_encendido_w
        self.umbral_terminado_w = umbral_terminado_w
        self.tiempo_espera_s = tiempo_espera_s
        self.log = logging.getLogger("DetectorCiclo")
        self.reiniciar()

    def reiniciar(self) -> None:
        self.en_ciclo = False
        self.inicio_ciclo: Optional[float] = None
        self.inicio_bajo: Optional[float] = None

    def procesar(self, watts: float, ahora: float) -> Optional[float]:
        """
        Procesa una lectura. Si el ciclo acaba de terminar devuelve
        su duración en minutos; en cualquier otro caso devuelve None.
        """
        if not self.en_ciclo:
            if watts > self.umbral_encendido_w:
                self.en_ciclo = True
                self.inicio_ciclo = ahora
                self.inicio_bajo = None
                self.log.info(f"Ciclo iniciado ({watts:.1f} W).")
            return None

        if watts <= self.umbral_terminado_w:
            if self.inicio_bajo is None:
                self.inicio_bajo = ahora
                self.log.info(f"Consumo bajo ({watts:.1f} W). Contando {self.tiempo_espera_s:.0f} s...")
            elif ahora - self.inicio_bajo >= self.tiempo_espera_s:
                duracion_min = (ahora - self.inicio_ciclo) / 60
                self.log.info(f"Ciclo terminado. Duración: {duracion_min:.0f} min.")
                self.reiniciar()
                return duracion_min
        elif self.inicio_bajo is not None:
            self.log.info(f"El consumo volvió a subir ({watts:.1f} W). Se reinicia el conteo.")
            self.inicio_bajo = None

        return None