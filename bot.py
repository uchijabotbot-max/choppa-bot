# -*- coding: utf-8 -*-
"""
Bot de Discord — "CHOPPA 🥷"
============================
Versión LEGAL: usa un bot oficial de aplicación (token de BOT del Portal de
Desarrolladores de Discord). NO es un selfbot, así que no arriesgas tu cuenta.

Qué hace:
- Se conecta como un bot normal y se ve directamente en Discord.
- Cambia el NOMBRE DEL BOT a variantes de "Choppa" con emojis, rotándolos
  cada pocos segundos en los servidores donde tenga permiso.
- Responde a comandos con prefijo "!" en Discord.

Cómo correrlo:
    1) Crea tu bot en https://discord.com/developers/applications
       (guía completa en README.md)
    2) Pon el token del bot en token.txt  (o en la variable DISCORD_TOKEN)
    3) .venv/Scripts/python bot.py          (Windows)
       .venv/bin/python bot.py              (Linux / Mac)
"""

import asyncio
import itertools
import os
import sys

# Evita que la terminal de Windows (cp1252) truene al imprimir emojis
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import discord
from discord.ext import commands

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

PREFIX = "!"

# Nombres que rota automáticamente
NICKNAMES = [
    "🥷 Choppa 🥷",
    "🔥🥷 Choppa 🔥",
    "😈 CHOPPA 😈",
    "🥷 Abajo Choppa 🔥",
    "⚡ ABAJO CHOPPA ⚡",
    "CHOPPA 🔥⚡",
    "🥷 Choppa ⚡",
    "ABAJO CHOPPA 😈🔥",
]

# Segundos entre cambio de nombre (no bajes de ~20 o Discord te rate-limitea)
ROTATE_INTERVAL = 30

# Estado que se muestra en el perfil del bot
STATUS_TEXT = "🥷 abajo choppa 🔥"

# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

def load_token() -> str:
    token = os.environ.get("DISCORD_TOKEN", "").strip()
    if token:
        return token
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            token = f.read().strip()
    except FileNotFoundError:
        pass
    if not token:
        raise SystemExit(
            "❌ No encontré el token.\n"
            "Pon el TOKEN DE BOT en el archivo token.txt "
            "o en la variable de entorno DISCORD_TOKEN."
        )
    return token


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True  # necesario para los comandos con prefijo "!"

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Control de rotación (encendida/apagada) por servidor
rotation_on: dict[int, bool] = {}
rotation_state: dict[int, object] = {}


def next_nickname(guild_id: int) -> str:
    """Devuelve el siguiente nombre de la rotación para un servidor."""
    names = NICKNAMES if rotation_on.get(guild_id, True) else [NICKNAMES[0]]
    state = rotation_state.setdefault(guild_id, itertools.cycle(names))
    return next(state)


async def set_nick(guild, nick: str) -> bool:
    """Intenta cambiar el nickname del bot, sin romper por errores."""
    try:
        await guild.me.edit(nick=nick)
        return True
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False


def can_change_nick(guild) -> bool:
    """¿El bot tiene permiso para cambiarse su propio nickname?"""
    me = guild.me
    if me is None:
        return False
    perms = me.guild_permissions
    return perms.manage_nicknames or perms.change_nickname


async def rotate_loop():
    """Cada ROTATE_INTERVAL segundos cambia el nombre en todos los servidores."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            if not rotation_on.get(guild.id, True):
                continue
            if can_change_nick(guild):
                await set_nick(guild, next_nickname(guild.id))
        await asyncio.sleep(ROTATE_INTERVAL)


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user} (ID: {bot.user.id})")
    print(f"   Servidores: {len(bot.guilds)}")
    try:
        await bot.change_presence(activity=discord.Game(name=STATUS_TEXT))
        print(f"   Estado: {STATUS_TEXT}")
    except discord.HTTPException as e:
        print(f"   ⚠️  No pude cambiar el estado: {e}")

    # Cambio inicial en todos los servidores
    for guild in bot.guilds:
        if can_change_nick(guild):
            if await set_nick(guild, next_nickname(guild.id)):
                print(f"   → {guild.name}: nombre cambiado")
            else:
                print(f"   ⚠️  {guild.name}: no pude cambiar el nombre")
        else:
            print(
                f"   ⚠️  {guild.name}: sin permiso — invita al bot con "
                f"'Gestionar apodos' (Manage Nicknames)"
            )

    print("🥷 ¡Choppa listo! Escribe !ayuda en Discord.")


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

@bot.command(name="ayuda", aliases=["help", "comandos"])
async def ayuda(ctx):
    await ctx.send(
        "🥷 **COMANDOS CHOPPA**\n"
        "`!choppa` → pone el nombre 🥷 Choppa 🥷\n"
        "`!abajo` → pone 🥷 ABAJO CHOPPA 🔥\n"
        "`!nombre <texto>` → pone un nombre personalizado (máx. 32 caracteres)\n"
        "`!estado <texto>` → cambia el estado del perfil\n"
        "`!rotar` → activa la rotación automática de nombres\n"
        "`!norotar` → apaga la rotación (queda el nombre actual)\n"
        "`!ayuda` → muestra esta lista\n"
        "⚙️ La rotación cambia el nombre cada 30 segundos."
    )


@bot.command(name="choppa")
async def choppa(ctx):
    nick = "🥷 Choppa 🥷"
    if await set_nick(ctx.guild, nick):
        await ctx.send(f"Nombre cambiado a **{nick}**")
    else:
        await ctx.send(
            "❌ No tengo permiso para cambiar mi nickname aquí. "
            "Invítame con el permiso 'Gestionar apodos' (Manage Nicknames)."
        )


@bot.command(name="abajo")
async def abajo(ctx):
    nick = "🥷 ABAJO CHOPPA 🔥"
    if await set_nick(ctx.guild, nick):
        await ctx.send(f"**{nick}**")
    else:
        await ctx.send(
            "❌ No tengo permiso para cambiar mi nickname aquí. "
            "Invítame con el permiso 'Gestionar apodos' (Manage Nicknames)."
        )


@bot.command(name="nombre", aliases=["nick"])
async def nombre(ctx, *, texto: str):
    nick = texto.strip()[:32]  # Discord limita a 32 caracteres
    if not nick:
        await ctx.send("❌ Escribe un nombre, ej: `!nombre 🥷 Choppa 🥷`")
        return
    if await set_nick(ctx.guild, nick):
        await ctx.send(f"✅ Nombre cambiado a **{nick}**")
    else:
        await ctx.send(
            "❌ No tengo permiso para cambiar mi nickname aquí. "
            "Invítame con el permiso 'Gestionar apodos' (Manage Nicknames)."
        )


@bot.command(name="estado", aliases=["status"])
async def estado(ctx, *, texto: str):
    try:
        await bot.change_presence(activity=discord.Game(name=texto.strip()[:128]))
        await ctx.send(f"✅ Estado cambiado a **{texto.strip()}**")
    except discord.HTTPException:
        await ctx.send("❌ No pude cambiar el estado.")


@bot.command(name="rotar")
async def rotar(ctx):
    rotation_on[ctx.guild.id] = True
    await ctx.send("✅ Rotación de nombres **activada**")


@bot.command(name="norotar", aliases=["parar"])
async def norotar(ctx):
    rotation_on[ctx.guild.id] = False
    await ctx.send("⏸️ Rotación **apagada** — el nombre queda como está.")


# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    bot.loop.create_task(rotate_loop())
    bot.run(load_token())
