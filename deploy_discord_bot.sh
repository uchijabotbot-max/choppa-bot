#!/usr/bin/env bash
# ============================================================================
# deploy_discord_bot.sh — Despliegue del bot Choppa en Oracle Cloud Free Tier
# ============================================================================
# Instala tu bot de Discord en una VM Oracle Cloud gratis para SIEMPRE.
#
# Requisitos:
#   1. Crea una cuenta gratis en https://cloud.oracle.com/free
#   2. Crea una VM Ubuntu (ARM Ampere, 4 cores, 24GB RAM gratis)
#   3. Conéctate por SSH
#   4. Ejecuta este script
#
# Uso (dentro de la VM):
#   chmod +x deploy_discord_bot.sh && ./deploy_discord_bot.sh
# ============================================================================
set -euo pipefail

echo "=============================================================="
echo "  🥷 CHOPPA BOT — Deploy en Oracle Cloud Free"
echo "=============================================================="
echo ""

# ---------- Pedir token ----------
read -rp "Pega tu DISCORD_TOKEN: " DISCORD_TOKEN
if [ -z "$DISCORD_TOKEN" ]; then
    echo "❌ Necesito el token." >&2
    exit 1
fi

# ---------- Instalar dependencias ----------
echo ""
echo ">> Instalando Python y git..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip git

# ---------- Crear directorio ----------
BOT_DIR="$HOME/choppa-bot"
mkdir -p "$BOT_DIR"
cd "$BOT_DIR"

# ---------- Clonar o actualizar ----------
REPO="https://github.com/uchijabotbot-max/choppa-bot.git"
if [ -d ".git" ]; then
    echo ">> Actualizando código..."
    git pull
else
    echo ">> Clonando bot..."
    git clone "$REPO" .
fi

# ---------- Instalar dependencias de Python ----------
echo ">> Instalando dependencias de Python..."
pip3 install --break-system-packages -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt

# ---------- Crear archivo de token ----------
echo "$DISCORD_TOKEN" > token.txt
chmod 600 token.txt

# ---------- Crear servicio systemd ----------
echo ">> Creando servicio del bot..."

# Obtener la IP pública
VM_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

sudo tee /etc/systemd/system/choppa-bot.service >/dev/null <<EOF
[Unit]
Description=Choppa Discord Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$BOT_DIR
ExecStart=$(which python3) $BOT_DIR/bot.py
Restart=always
RestartSec=5
Environment=DISCORD_TOKEN=$DISCORD_TOKEN
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# ---------- Iniciar servicio ----------
echo ">> Iniciando bot..."
sudo systemctl daemon-reload
sudo systemctl enable choppa-bot
sudo systemctl restart choppa-bot

sleep 3

# ---------- Verificar ----------
echo ""
if sudo systemctl is-active --quiet choppa-bot; then
    echo "=============================================================="
    echo "  ✅ ¡CHOPPA BOT ESTÁ CORRIENDO!"
    echo "=============================================================="
    echo ""
    echo "  🌐 IP de la VM: $VM_IP"
    echo "  📁 Directorio: $BOT_DIR"
    echo ""
    echo "  Comandos útiles:"
    echo "    Ver estado:     sudo systemctl status choppa-bot"
    echo "    Ver logs:       sudo journalctl -u choppa-bot -f"
    echo "    Reiniciar:      sudo systemctl restart choppa-bot"
    echo "    Detener:        sudo systemctl stop choppa-bot"
    echo "    Actualizar:     cd $BOT_DIR && git pull && sudo systemctl restart choppa-bot"
    echo ""
    echo "  El bot se reinicia SOLO si se cae."
    echo "  Se inicia SOLO al reiniciar la VM."
    echo "=============================================================="
else
    echo "❌ Hubo un error. Mira los logs:"
    echo "   sudo journalctl -u choppa-bot -n 20"
fi
