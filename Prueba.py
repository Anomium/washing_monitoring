import asyncio
import logging

from Configuracion import Configuracion
from MonitorLavadora import MonitorLavadora

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(name)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

async def main() -> None:
    monitor = MonitorLavadora.desde_configuracion(Configuracion())
    await monitor.ejecutar()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor detenido.")