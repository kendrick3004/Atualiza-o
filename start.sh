#!/bin/bash

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

# Função para ativar manutenção
start_maintenance() {
    if [ -d "$BASE_DIR/maintenance" ]; then
        log "🚧 Iniciando modo manutenção..."
        (nohup python3 "$BASE_DIR/maintenance/main.py" >> "$MAINTENANCE_LOG" 2>&1 &)
        sleep 2
        log "✅ Manutenção ativa na porta 5000"
    else
        log "❌ Erro: pasta maintenance não encontrada em $BASE_DIR/maintenance"
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
# ------------------ LIMPA ------------------
log "🧹 Limpando arquivos de index/site antigo..."
rm -rf "$BASE_DIR/site"

# ------------------ DOWNLOAD ------------------
log "📥 Acessando repositórios para atualização..."

mkdir -p "$BASE_DIR/site"
cd "$BASE_DIR/site" || exit 1

log "⏳ Extraindo dados do repositório com Sparse Checkout..."
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Configurações de timeout e retry para git
export GIT_CONNECT_TIMEOUT=120
export GIT_HTTP_CONNECT_TIMEOUT=120

RETRY_COUNT=0
MAX_RETRIES=3
CLONE_SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$CLONE_SUCCESS" = false ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -gt 1 ]; then
        log "🔄 Tentativa $RETRY_COUNT de $MAX_RETRIES..."
        sleep 5
        rm -rf .git
    fi
    
    log "📊 Iniciando clonagem..."
    
    # 🎯 BARRINHA + % + VELOCIDADE - SÓ UMA LINHA LIMPA!
   timeout 600 git clone --depth=1 --single-branch --branch main --progress https://github.com/kendrick3004/Atualiza-o.git . >> "$GIT_LOG" 2>&1 &
    GIT_PID=$!
    
    while kill -0 $GIT_PID 2>/dev/null; do
        percent=$(tail -20 "$GIT_LOG" | grep -o "[0-9]\+%" | tail -1 | tr -d "%" || echo "0")
        speed=$(tail -5 "$GIT_LOG" | grep -o "[0-9]\+\.[0-9]\+ [KMG]iB/s" | tail -1 || echo "")
        filled=$((percent * 50 / 100))
        bar=""; for ((i=0;i<filled;i++)); do bar+="█"; done; for ((i=filled;i<50;i++)); do bar+="░"; done
        printf "\r📥 Baixando: [%-50s] %3d%% - %s" "$bar" "$percent" "$speed"
        sleep 0.5
    done
   
    wait $GIT_PID
    echo ""
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log "✓ Clone concluído, checando integridade..."
        if [ -f "index.html" ] || [ -f "site/index.html" ]; then
            log "✓ Arquivos do site intactos, clonagem bem-sucedida"
            CLONE_SUCCESS=true
        else
            log "⚠️  Site não encontrado, tentando novamente..."
        fi
    else
        log "⚠️  Git clone falhou ou timeout"
    fi
done

if [ "$CLONE_SUCCESS" = true ]; then
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    log "📂 Configurando sparse checkout (site)..."
    if git sparse-checkout init --cone 2>&1 | tee -a "$GIT_LOG"; then
        git sparse-checkout set site 2>&1 | tee -a "$GIT_LOG"
        log "✓ Sparse Checkout configurado"
    else
        log "⚠️  Sparse checkout não disponível, usando clone completo"
    fi
    
    log "✅ Download concluído com sucesso"
else
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "❌ Erro no download após $MAX_RETRIES tentativas (ver log em: $GIT_LOG)"
    exit 1
fi

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
    cd "$BASE_DIR/site" && nohup python3 main.py >> "$SITE_LOG" 2>&1 &
    sleep 3
    
    if pgrep -f "python3 main.py" > /dev/null; then
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
    log "🔔 Por favor, verifique o serviço 'cloudflared' ou o token no setup.sh."
fi

log "📊 Logs salvos em: $LOG_DIR"
log "🌐 Site disponível através do túnel Cloudflare."
