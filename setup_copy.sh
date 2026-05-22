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
# Os pacotes do sistema (nano, curl, wget, openssh-server, net-tools, git, python3, python3-pip, python3-venv) devem ser instalados manualmente antes de executar este script.
log "[2/3] Instalando pacotes do sistema e dependencias Python"
sudo apt install -y nano curl wget openssh-server net-tools git python3 python3-pip python3-venv
sudo pip3 install flask python-dotenv werkzeug --break-system-packages || sudo pip3 install flask python-dotenv werkzeug

log "[3/3] Configurando o Cloudflared Tunnel (Persistente)"
# Add cloudflare gpg key
log "Adicionando chave GPG do Cloudflare..."
sudo mkdir -p --mode=0755 /usr/share/keyrings
# Adicionar chave GPG
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
    export $(cat .env | xargs)
    log "✅ Variaveis de ambiente carregadas com sucesso"
else
    log "❌ ERRO: Arquivo .env nao encontrado na raiz do projeto"
    log "❌ Certifique-se de que o arquivo .env existe e contém CLOUDFLARED_TOKEN"
    exit 1
fi

# Validar que o token Cloudflare foi carregado
if [ -z "$CLOUDFLARED_TOKEN" ]; then
    log "❌ ERRO: CLOUDFLARED_TOKEN nao esta definido no arquivo .env"
    log "❌ Adicione a variavel CLOUDFLARED_TOKEN ao arquivo .env e tente novamente"
    exit 1
fi

TOKEN=$CLOUDFLARED_TOKEN

log "Instalando Cloudflare Tunnel como serviço do sistema (systemd)..."
# Remove serviço antigo se existir para garantir atualização do token
log "Removendo serviço antigo (se existir)..."
sudo cloudflared service uninstall || true
log "Serviço antigo removido"

# Instala como serviço - isso garante que ele inicie com o sistema e rode independente do Flask
log "Instalando novo serviço com token atualizado..."
sudo cloudflared tunnel run $TOKEN
log "Serviço instalado com sucesso"

# Garante que o serviço esteja habilitado e rodando
log "Habilitando serviço systemd..."
sudo systemctl enable cloudflared || true
log "Serviço habilitado"

log "Iniciando serviço Cloudflare..."
sudo systemctl start cloudflared || true
log "Serviço iniciado"

log "================================================"
log "✅ Setup concluído com sucesso!"
log "O Cloudflare Tunnel agora é um serviço persistente."
log "Ele continuará rodando mesmo em modo de manutenção."
log "Ativando o start.sh para iniciar o site..."
sudo chmod +x "$PWD/start.sh"
log "Permissões de execução configuradas"

log "Executando start.sh..."
"$PWD/start_copy.sh"
log "================================================"
