#!/bin/bash

# ==============================================================================
# start_copy.sh - Script de Deploy e Inicialização Local (Sem Download)
# ==============================================================================
# Descrição:
#   Este script é responsável por inicializar o servidor utilizando os arquivos
#   já existentes na pasta local 'site' (sem baixar do GitHub):
#   1. Encerra servidores existentes (site e manutenção).
#   2. Ativa o modo de manutenção temporário na porta 5000.
#   3. Mantém a pasta 'site' existente (não apaga nem clona nada do GitHub).
#   4. Reconstrói/atualiza a estrutura do banco de dados (generate_assets_structure.py).
#   5. Verifica a conectividade do Cloudflare Tunnel.
#   6. Encerra a manutenção e inicia o servidor do site principal.
#   7. Se houver falhas na inicialização do site ou do túnel, restaura a manutenção.
#
# Diferenças chave vs start.sh:
#   - start.sh: Executa clonagem limpa do GitHub a cada deploy (ideal para produção).
#   - start_copy.sh: Pula o download e usa os arquivos locais na pasta 'site'
#     (ideal para desenvolvimento ou deploys offline rápidos).
# ==============================================================================

set -u

# Pega o diretório onde o script está localizado
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

LOG_DIR="$BASE_DIR/logs/$(date +%Y-%m-%d)"
mkdir -p "$LOG_DIR"

MAINTENANCE_LOG="$LOG_DIR/maintenance.log"
SITE_LOG="$LOG_DIR/site.log"
DATABASE_LOG="$LOG_DIR/database.log"
GIT_LOG="$LOG_DIR/git.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

# Função para ativar manutenção
start_maintenance() {
    if [ -d "$BASE_DIR/maintenance" ]; then
        log "🚧 Iniciando modo manutenção..."
        pkill -f "$BASE_DIR/site/main.py" 2>/dev/null || true
        (nohup python3 "$BASE_DIR/maintenance/main.py" >> "$MAINTENANCE_LOG" 2>&1 &)
        sleep 2
        log "✅ Manutenção ativa na porta 5000"
    else
        log "❌ Erro: pasta maintenance não encontrada em $BASE_DIR/maintenance"
    fi
}

# Função para verificar o Cloudflare Tunnel
check_cloudflare() {
    log "🔍 Verificando Cloudflare Tunnel..."
    # Verifica se o serviço systemd do cloudflared está ativo
    if systemctl is-active --quiet cloudflared; then
        log "✅ Cloudflare Tunnel está rodando corretamente!"
        return 0
    else
        # Tenta verificar se há algum processo cloudflared rodando caso não seja serviço
        if pgrep -x "cloudflared" > /dev/null; then
            log "✅ Cloudflare Tunnel (processo) está rodando!"
            return 0
        fi
        log "❌ Cloudflare Tunnel NÃO está rodando!"
        return 1
    fi
}

# Função para parar servidores
stop_servers() {
    log "🛑 Parando servidores de sites..."
    pkill -f main.py 2>/dev/null || true
    pkill -f "maintenance/main.py" 2>/dev/null || true
    sleep 2
}

# --- INÍCIO DO PROCESSO ---

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "🚀 INICIANDO PROCESSO DE DEPLOY"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

stop_servers
start_maintenance

# ------------------ DOWNLOAD (COMENTADO PARA PRESERVAR MELHORIAS) ------------------

# ------------------ DATABASE ------------------
log "🗄️ Verificando estrutura do database..."
if [ -d "$BASE_DIR/database" ]; then
    log "🔎 Gerando estrutura philistudies.json..."
    # O script de geração agora está na pasta database raiz
    if [ -f "$BASE_DIR/database/generate_assets_structure.py" ]; then
        if python3 "$BASE_DIR/database/generate_assets_structure.py" >> "$DATABASE_LOG" 2>&1; then
            log "✅ Database estruturado com sucesso!"
        else
            log "❌ Erro na geração do database (ver log em: $DATABASE_LOG)"
        fi
    fi
else
    log "❌ Pasta database não encontrada!"
fi

# ------------------ VERIFICAÇÃO FINAL E START ------------------

# Verifica o Cloudflare antes de subir o site
if check_cloudflare; then
    log "🛑 Encerrando servidor de manutenção..."
    pkill -f "maintenance/main.py" 2>/dev/null || true
    sleep 2
    
    log "🚀 Iniciando servidor do site..."
    if cd "$BASE_DIR/site"; then
        nohup python3 main.py >> "$SITE_LOG" 2>&1 &
    else
        log "❌ Erro ao acessar diretório do site para iniciar o servidor"
        exit 1
    fi
    sleep 3

    if pgrep -f "python3 main.py" > /dev/null 2>&1; then
        log "✅ Servidor do site iniciado com sucesso!"
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        log "✅ DEPLOY FINALIZADO COM SUCESSO!"
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        log "❌ Falha ao iniciar o servidor do site. Ativando manutenção de emergência..."
        start_maintenance
    fi
else
    log "⚠️ Cloudflare Tunnel falhou. Mantendo modo manutenção para segurança."
    log "🔔 Por favor, verifique o serviço 'cloudflared' ou as variáveis de ambiente."
fi

log "📊 Logs salvos em: $LOG_DIR"
log "🌐 Site disponível através do túnel Cloudflare."
