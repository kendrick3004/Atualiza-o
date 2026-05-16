#!/bin/bash

# Script para configurar um único túnel Cloudflare
# O usuário solicitou apenas um túnel rodando.

TOKEN="eyJhIjoiOWNjZGQzMjk0NDllMzJhZWU4YzRkYWRkMDZjOGM0NzciLCJ0IjoiMzQ3NDczMGYtZjMwZi00ZGEyLWE4ZjAtYzBhYmJjZTVhNDBjIiwicyI6Ik5qZ3hOREEwTURjdFpHUmpOQzAwTVdFMExUbGpNRFF0TURZME9EWXhObVpoWTJVdyJ9"

echo "--- Removendo túneis antigos ---"
sudo systemctl stop cloudflared-database || true
sudo systemctl disable cloudflared-database || true
sudo rm -f /etc/systemd/system/cloudflared-database.service || true
sudo systemctl daemon-reload || true

sudo cloudflared service uninstall || true

echo "--- Instalando Túnel Único ---"
sudo cloudflared service install $TOKEN
sudo systemctl enable cloudflared
sudo systemctl start cloudflared

echo "✅ Túnel único configurado com sucesso!"
