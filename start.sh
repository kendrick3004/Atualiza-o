#!/bin/bash

# ==============================================================================
# start.sh - Script de Deploy e Inicialização Completa
# ==============================================================================
# Descrição:
#   Este script é responsável por realizar o fluxo completo de deploy do site:
#   1. Encerra servidores existentes (site e manutenção).
#   2. Ativa o modo de manutenção temporário na porta 5000.
#   3. Realiza o download (git clone com timeout) da última versão do repositório
#      público (https://github.com/kendrick3004/Atualiza-o.git) em uma pasta temporária.
#   4. Copia os novos arquivos para a pasta 'site'.
#   5. Reconstrói/atualiza a estrutura do banco de dados (generate_assets_structure.py).
#   6. Verifica a conectividade do Cloudflare Tunnel.
#   7. Encerra a manutenção e inicia o servidor do site principal.
#   8. Se houver falhas na inicialização do site ou do túnel, restaura a manutenção.
#
# Diferenças chave vs start_copy.sh:
#   - start.sh: Executa clonagem limpa do GitHub a cada deploy (ideal para produção).
#   - start_copy.sh: Pula o download e usa os arquivos locais na pasta 'site'
#     (ideal para desenvolvimento ou deploys offline rápidos).
# ==============================================================================

set -u

# Carregar variaveis de ambiente do arquivo .env
if [ -f ".env" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        # Remove espacos no inicio e fim
        cleaned_line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        # Pula se for vazio ou comecar com #
        [[ -z "$cleaned_line" ]] && continue
        [[ "$cleaned_line" =~ ^# ]] && continue
        # Exporta a variavel
        export "$cleaned_line"
    done < .env
else
    echo "⚠️ Aviso: Arquivo .env nao encontrado. Algumas funcionalidades podem nao funcionar."
fi

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
# ------------------ LIMPA ------------------
log "🧹 Limpando arquivos de index/site antigo..."
rm -rf "$BASE_DIR/site"
mkdir -p "$BASE_DIR/site"

# ------------------ CONFIG TEMP ------------------

# Pasta temporária fixa (já existente)
TEMP_DIR="$BASE_DIR/.temp"

# Nome da pasta do repositório temporário
TEMP_REPO="$TEMP_DIR/.repo"

# Limpa apenas a clonagem anterior
rm -rf "$TEMP_REPO"

# ------------------ DOWNLOAD ------------------

log "📥 Acessando repositórios para atualização..."
cd "$TEMP_DIR" || exit 1

log "⏳ Extraindo dados do repositório..."
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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
        rm -rf "$TEMP_REPO"
    fi

    log "📊 Iniciando clonagem..."

    timeout 1200 git clone \
        --depth=1 \
        --single-branch \
        --branch main \
        --progress \
        https://github.com/kendrick3004/Atualiza-o.git \
        "$TEMP_REPO" \
        >> "$GIT_LOG" 2>&1 &

    GIT_PID=$!

    while kill -0 $GIT_PID 2>/dev/null; do
        percent=$(tail -20 "$GIT_LOG" | grep -o "[0-9]\+%" | tail -1 | tr -d "%" || echo "0")
        speed=$(tail -5 "$GIT_LOG" | grep -o "[0-9]\+\.[0-9]\+ [KMG]iB/s" | tail -1 || echo "")
        filled=$((percent * 50 / 100))
        bar=""
        for ((i=0;i<filled;i++)); do bar+="█"; done
        for ((i=filled;i<50;i++)); do bar+="░"; done
        printf "\r📥 Baixando: [%-50s] %3d%% - %s" "$bar" "$percent" "$speed"
        sleep 0.5
    done

    wait $GIT_PID
    echo ""

    if [ $? -eq 0 ]; then
        log "✓ Clone concluído, verificando integridade..."
        if [ -d "$TEMP_REPO/site" ]; then
            log "✓ Repositório válido"
log "📂 Copiando arquivos do site..."

SOURCE_DIR="$TEMP_REPO/site"
DEST_DIR="$BASE_DIR/site"

# Conta total de arquivos
TOTAL_FILES=$(find "$SOURCE_DIR" -type f | wc -l)

CURRENT_FILE=0

# Copia mantendo estrutura
find "$SOURCE_DIR" -type f | while read -r file; do

    # Caminho relativo
    REL_PATH="${file#$SOURCE_DIR/}"

    # Pasta destino
    DEST_PATH="$DEST_DIR/$REL_PATH"

    # Cria diretório destino
    mkdir -p "$(dirname "$DEST_PATH")"

    # Copia arquivo
    cp "$file" "$DEST_PATH"

    CURRENT_FILE=$((CURRENT_FILE + 1))

    # Percentual
    percent=$((CURRENT_FILE * 100 / TOTAL_FILES))

    # Barra visual
    filled=$((percent * 50 / 100))

    bar=""
    for ((i=0;i<filled;i++)); do
        bar+="█"
    done

    for ((i=filled;i<50;i++)); do
        bar+="░"
    done

    printf "\r📂 Copiando: [%-50s] %3d%% (%d/%d)" \
        "$bar" \
        "$percent" \
        "$CURRENT_FILE" \
        "$TOTAL_FILES"

done

echo ""
log "✅ Arquivos copiados com sucesso!"

            CLONE_SUCCESS=true

        else
            log "⚠️ Pasta site não encontrada no repositório"
        fi

    else
        log "⚠️ Git clone falhou ou timeout"
    fi
done

if [ "$CLONE_SUCCESS" = true ]; then

    log "🧹 Limpando arquivos temporários..."
    rm -rf "$TEMP_REPO"
    log "✅ Download concluído com sucesso"
else
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "❌ Erro no download após $MAX_RETRIES tentativas"
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
