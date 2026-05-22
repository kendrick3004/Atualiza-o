#!/bin/bash

# Setup inicial do ambiente para o site
set -e

# Função para logging com timestamp
log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

log "================================================"
log "🚀 Iniciando instalação de dependências e setup"
log "================================================"

# Atualiza repositórios
log "[1/3] Atualizando pacotes do sistema..."
sudo apt update

# Instala pacotes do sistema solicitados e essenciais
log "[2/3] Instalando pacotes do sistema e dependencias Python"
sudo apt install -y nano curl wget openssh-server net-tools git python3 python3-pip python3-venv

# No Ubuntu 24.04+ (Noble), o pip é bloqueado para evitar quebrar o sistema.
# O erro do 'blinker' ocorre porque o sistema tenta desinstalar uma versão do SO.
# Vamos usar --ignore-installed para forçar a nossa versão sem tentar remover a do sistema.
log "Instalando bibliotecas Python necessárias..."
sudo pip3 install flask python-dotenv werkzeug --break-system-packages --ignore-installed blinker || \
sudo pip3 install flask python-dotenv werkzeug --break-system-packages

log "[3/3] Configurando o Cloudflared Tunnel (Persistente)"
# Add cloudflare gpg key
log "Adicionando chave GPG do Cloudflare..."
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Adicionar repositório
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" | sudo tee /etc/apt/sources.list.d/cloudflared.list

# Instalar cloudflared
sudo apt-get update
sudo apt-get install cloudflared -y

log "Chave GPG adicionada com sucesso"

# Carregar variaveis de ambiente do arquivo .env (obrigatório)
log "Carregando variaveis de ambiente do .env..."
if [ -f ".env" ]; then
    # Usar uma forma mais segura de exportar variáveis
    set -a
    source .env
    set +a
    log "✅ Variaveis de ambiente carregadas com sucesso"
else
    log "❌ ERRO: Arquivo .env nao encontrado na raiz do projeto"
    exit 1
fi

# Validar que o token Cloudflare foi carregado
if [ -z "$CLOUDFLARED_TOKEN" ]; then
    log "❌ ERRO: CLOUDFLARED_TOKEN nao esta definido no arquivo .env"
    exit 1
fi

TOKEN=$CLOUDFLARED_TOKEN

log "Instalando Cloudflare Tunnel como serviço do sistema (systemd)..."
sudo cloudflared service uninstall || true
# Instala como serviço
sudo cloudflared service install $TOKEN || true
log "Serviço instalado com sucesso"

# Garante que o serviço esteja habilitado e rodando
sudo systemctl enable cloudflared || true
sudo systemctl start cloudflared || true
log "Serviço iniciado"

log "================================================"
log "✅ Setup concluído com sucesso!"
log "Ativando o start.sh para iniciar o site..."
sudo chmod +x "$PWD/start.sh"
log "Executando start.sh..."
"$PWD/start.sh"
log "================================================"
