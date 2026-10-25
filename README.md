# Smart – Aviso de fin de lavado

Programa en Python que vigila la lavadora y avisa cuando termina el ciclo, de dos formas a la vez:

- 🔊 **Alexa**: anuncio o notificación en tus dispositivos Echo.
- 🪟 **Windows**: notificación emergente (toast) en el escritorio.

## Cómo funciona

1. `MonitorLavadora` consulta periódicamente el estado de la lavadora (<p. ej. consumo eléctrico de un enchufe inteligente>).
2. Cuando detecta que el ciclo ha terminado (<p. ej. el consumo queda por debajo de X W durante Y minutos>), lanza el aviso.
3. `NotificadorMultiple` reparte el mensaje a todos los notificadores configurados:
   - `NotificadorAlexa`
   - `NotificadorWindows`

## Estructura

```
Smart/
├── Configuracion.py        # Carga la configuración desde .env
├── MonitorLavadora.py      # Lógica de detección del fin de ciclo
├── Prueba.py               # Script de arranque / prueba
├── Notificador/
│   ├── __init__.py
│   ├── Notificador.py          # Clase base
│   ├── NotificadorAlexa.py     # Aviso por Alexa
│   ├── NotificadorWindows.py   # Notificación de Windows
│   └── NotificadorMultiple.py  # Envía a varios notificadores a la vez
└── .env                    # Credenciales y parámetros (no subir a git)
```

## Requisitos

- Windows 10/11
- Python 3.10 o superior
- <Dispositivo para medir la lavadora, p. ej. enchufe inteligente con medición de consumo>
- Una cuenta de Amazon con un dispositivo Alexa
- <Servicio o skill usado para enviar avisos a Alexa>

## Instalación

```powershell
git clone <url-del-repositorio>
cd Smart
py -m pip install python-dotenv <otras dependencias>
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
# Alexa
ALEXA_<VARIABLE>=<valor>

# Lavadora / dispositivo de medición
<VARIABLE>=<valor>

# Detección del fin de ciclo
UMBRAL_POTENCIA_W=<valor>
MINUTOS_ESPERA=<valor>
INTERVALO_CONSULTA_SEG=<valor>
```

> ⚠️ Añade `.env` al `.gitignore` para no publicar tus credenciales.

## Uso

```powershell
py Prueba.py
```

Deja el programa abierto mientras lava la lavadora. Cuando termine el ciclo, recibirás el aviso en Alexa y en Windows.

## Añadir otro tipo de aviso

Crea una clase nueva en `Notificador/` que herede de `Notificador`, impleméntale el método de envío y regístrala en `NotificadorMultiple`.

## Solución de problemas

| Problema | Causa probable |
|---|---|
| `ModuleNotFoundError: dotenv` | Falta instalar: `py -m pip install python-dotenv` |
| No llega el aviso a Alexa | Credenciales del `.env` incorrectas o caducadas |
| No aparece la notificación de Windows | Notificaciones desactivadas o modo "No molestar" activo |
| Avisa antes de que termine | El umbral de consumo es demasiado alto o el tiempo de espera, demasiado corto |
