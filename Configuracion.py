from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

def _env(name: str, default: str = ""):
    return field(default_factory=lambda: os.getenv(name, default))

@dataclass(frozen=True)
class Configuracion:
    # Enchufe
    ip: str = _env("KASA_IP")
    usuario: str = _env("KASA_USUARIO")
    clave: str = _env("KASA_CLAVE")


    # Alexa (Voice Monkey) — dejar vacío para desactivar
    alexa_token: str = _env("ALEXA_TOKEN")
    alexa_dispositivo: str = _env("ALEXA_DISPOSITIVO")

    # Detección
    umbral_terminado_w: float = 2.0   # <= este valor = lavadora detenida
    umbral_encendido_w: float = 5.0   # >  este valor = empezó un ciclo
    umbral_prendida_w: float = 0.5    # >  este valor al iniciar la app = lavadora prendida sin ciclo
    tiempo_espera_s: float = 120      # 2 minutos seguidos en consumo bajo

    # Tiempos del bucle
    intervalo_s: float = 5            # how often the consumption is read
    reintento_s: float = 30