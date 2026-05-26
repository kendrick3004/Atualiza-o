#!/bin/bash

# ==============================================================================
# start_maintenance.sh - Script de Deploy de Manutenção e Repositório Alternativo
# ==============================================================================
# Descrição:
#   Este script realiza um deploy limpando a pasta 'site' e fazendo o download
#   de uma versão completa a partir de um repositório DIFERENTE do start.sh:
#   1. Encerra qualquer servidor em execução.
#   2. Ativa o modo manutenção a partir da pasta 'maintenance'.
#   3. Remove e recria a pasta 'site'.
#   4. Executa git clone do repositório secundário (kendrick3004/site.git).
#   5. Executa a estruturação do banco de dados (generate_assets_structure.py).
#   6. Desativa o modo manutenção e inicia o servidor principal do site.
#
# Diferenças chave vs start.sh:
#   - start_maintenance.sh: Clona a partir de 'https://github.com/kendrick3004/site.git'.
#   - start.sh: Clona a partir de 'https://github.com/kendrick3004/Atualiza-o.git'.
# ==============================================================================

set -u

# Pega o diretório onde o script está localizado (raiz do projeto /index)
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_BASE_DIR="$BASE_DIR/logs"
HOJE=$(date +%Y-%m-%d)
DIA_LOG_DIR="$LOG_BASE_DIR/$HOJE"
MAINTENANCE_LOG="$DIA_LOG_DIR/maintenance_system.log"
SITE_LOG="$DIA_LOG_DIR/site_system.log"
DATABASE_LOG="$DIA_LOG_DIR/database_structure.log"

mkdir -p "$DIA_LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "📂 Diretório base: $BASE_DIR"
cd "$BASE_DIR" || exit 1

log "🛑 Parando qualquer servidor em execução..."
pkill -f main.py >/dev/null 2>&1 || true
sleep 2

log "🚧 Iniciando modo manutenção..."
if [ -d "$BASE_DIR/maintenance" ]; then
    cd "$BASE_DIR/maintenance" || exit 1
    nohup python3 main.py >> "$MAINTENANCE_LOG" 2>&1 &
    cd "$BASE_DIR" || exit 1
    sleep 3
    log "✅ Modo manutenção iniciado com sucesso."
else
    log "❌ Erro: pasta maintenance não encontrada em $BASE_DIR/maintenance"
fi

log "🧹 Limpando a pasta site para um download novo..."
rm -rf "$BASE_DIR/site"

log "📥 Baixando versão completa do GitHub..."
if ! git clone https://github.com/kendrick3004/site.git "$BASE_DIR/site"; then
    log "❌ Erro: falha ao baixar o site do GitHub."
    log "📊 Logs do dia salvos em: $DIA_LOG_DIR"
    exit 1
fi

log "📂 Validando a pasta do site..."
if [ ! -d "$BASE_DIR/site" ]; then
    log "❌ Erro: a pasta site não foi criada após o clone."
    log "📊 Logs do dia salvos em: $DIA_LOG_DIR"
    exit 1
fi

cd "$BASE_DIR/site" || exit 1
log "✅ Pasta do site encontrada com sucesso."

log "🔎 Verificando estrutura do database..."
if [ -d "$BASE_DIR/site/database" ]; then
    log "✅ Pasta database encontrada em $BASE_DIR/site/database"
else
    log "❌ Erro: pasta database não encontrada em $BASE_DIR/site/database"
fi

if [ -f "$BASE_DIR/site/database/generate_assets_structure.py" ]; then
    log "✅ Script Python encontrado: $BASE_DIR/site/database/generate_assets_structure.py"
else
    log "❌ Erro: script Python de estrutura não encontrado."
fi

if [ -d "$BASE_DIR/site/database/assets" ]; then
    log "✅ Pasta assets encontrada. Iniciando geração da estrutura do database..."
    cd "$BASE_DIR/site/database" || exit 1

    if python3 generate_assets_structure.py >> "$DATABASE_LOG" 2>&1; then
        if [ -f "$BASE_DIR/site/database/file_structure.json" ]; then
            log "✅ Sucesso na procura da pasta e na geração da estrutura do database."
            log "✅ Arquivo gerado: $BASE_DIR/site/database/file_structure.json"
        else
            log "❌ Erro: o Python executou, mas o arquivo file_structure.json não foi encontrado."
        fi
    else
        log "❌ Erro na execução do Python ao gerar a estrutura do database. Consulte $DATABASE_LOG"
    fi

    cd "$BASE_DIR/site" || exit 1
else
    log "❌ Erro na procura da pasta assets: $BASE_DIR/site/database/assets não encontrada."
fi

log "🛑 Finalizando modo manutenção..."
pkill -f main.py >/dev/null 2>&1 || true
sleep 2

log "🚀 Iniciando servidor principal do site..."
if cd "$BASE_DIR/site"; then
    nohup python3 main.py >> "$SITE_LOG" 2>&1 &
    log "✅ Deploy finalizado. Site online na porta 5000."
else
    log "❌ Erro ao acessar diretório do site para iniciar o servidor"
    exit 1
fi
log "📊 Logs do dia salvos em: $DIA_LOG_DIR"
