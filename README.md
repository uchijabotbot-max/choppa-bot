# 🥷 CHOPPA Bot

Bot **oficial y legal** de Discord (una *aplicación bot* creada en el Portal de Desarrolladores — NO es un selfbot, no usas el token de tu cuenta personal, así que **no te banean**). Se conecta como bot y se ve directamente en Discord (no es una página web). Cambia el nombre del bot a **"Choppa"** con emojis, rotándolos automáticamente, y responde a comandos con el prefijo `!`.

## 📦 Instalación

Requiere **Python 3.10+** (probado con 3.14).

```bash
# 1) Entorno virtual + dependencias (solo la primera vez)
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows
.venv/bin/pip install -r requirements.txt         # Linux / Mac

# 2) Tu token de bot
cp token.txt.example token.txt                    # Windows: copia el archivo manualmente
#   → pega tu token dentro de token.txt (o usa la variable DISCORD_TOKEN)
```

## 🤖 Crear el bot (una sola vez, en discord.com)

1. Entra a [Portal de Desarrolladores](https://discord.com/developers/applications) → **New Application** → ponle nombre (ej: `Choppa`).
2. Pestaña **Bot** → **Reset Token** → copia el token y pégalo en `token.txt`.
3. En la misma pestaña **Bot**, activa el interruptor **MESSAGE CONTENT INTENT** (sin esto los comandos `!` no funcionan).
4. Invítalo a tu servidor con este enlace (reemplaza `TU_ID_DE_BOT` por el **Application ID** que aparece arriba a la izquierda de tu aplicación):

```
https://discord.com/oauth2/authorize?client_id=TU_ID_DE_BOT&permissions=201411584&scope=bot
```

> Los permisos del enlace incluyen: ver canales, enviar mensajes, ver historial y **Gestionar apodos** (Manage Nicknames), que es lo que el bot necesita para cambiarse el nombre.

## 🚀 Ejecutar

```bash
.venv/Scripts/python bot.py     # Windows
.venv/bin/python bot.py         # Linux / Mac
```

Al arrancar verás en la terminal `✅ Conectado como Choppa...` y el bot cambiará su nombre en todos los servidores donde tenga permiso.

## 🎮 Comandos (en Discord)

| Comando | Qué hace |
|---|---|
| `!ayuda` | Muestra la lista de comandos |
| `!choppa` | Pone el nombre **🥷 Choppa 🥷** |
| `!abajo` | Pone **🥷 ABAJO CHOPPA 🔥** |
| `!nombre <texto>` | Pone un nombre personalizado (máx. 32 caracteres) |
| `!estado <texto>` | Cambia el estado del perfil (ej: `!estado 🥷 abajo choppa 🔥`) |
| `!rotar` | Activa la rotación automática de nombres |
| `!norotar` | Apaga la rotación |

La rotación automática cambia el nombre cada **30 segundos** en todos los servidores donde el bot tenga permiso (los nombres están en la lista `NICKNAMES` dentro de `bot.py` — edítala a tu gusto).

## 🧠 Personalizar

- **Nombres a rotar:** edita la lista `NICKNAMES` en `bot.py`.
- **Velocidad de rotación:** cambia `ROTATE_INTERVAL` (en segundos). No lo pongas por debajo de ~20 o Discord aplica rate-limit.
- **Estado del perfil:** cambia `STATUS_TEXT`.

## ❓ Problemas comunes

- **El bot no responde a comandos** → revisa que activaste el **MESSAGE CONTENT INTENT** en el Portal y que lo invitaste con `permissions=201411584` (o al menos con el permiso de enviar mensajes).
- **"No tengo permiso para cambiar mi nickname"** → reinvita al bot con el permiso **Gestionar apodos** (Manage Nicknames) usando el enlace de arriba.
- **"New login detected"** → ese aviso es de los selfbots; con un bot oficial no aparece.
