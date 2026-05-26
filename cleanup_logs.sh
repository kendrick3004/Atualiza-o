#!/bin/bash

# ==============================================================================
# cleanup_logs.sh - Script de Limpeza de Logs Antigos
# ==============================================================================
# Descrição:
#   Remove diretórios de log com data superior à quantidade de dias especificada.
#   Apenas diretórios com o formato AAAA-MM-DD localizados em logs/ serão avaliados
#   para garantir a segurança do processo.
#
# Uso:
#   ./cleanup_logs.sh [dias] [--dry-run]
#
# Parâmetros:
#   dias       : Opcional. Número de dias limite para manter os logs (padrão: 90).
#   --dry-run  : Opcional. Apenas exibe o que seria removido, sem excluir nada.
# ==============================================================================

set -u

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGS_DIR="$BASE_DIR/logs"
DAYS=90
DRY_RUN=false

# Tratar argumentos
for arg in "$@"; do
    if [ "$arg" = "--dry-run" ]; then
        DRY_RUN=true
    elif [[ "$arg" =~ ^[0-9]+$ ]]; then
        DAYS="$arg"
    fi
done

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🧹 Iniciando limpeza de logs (limite: $DAYS dias)..."
if [ "$DRY_RUN" = true ]; then
    log "🔍 Modo de simulação (--dry-run) ativo. Nenhuma alteração real será feita."
fi

if [ ! -d "$LOGS_DIR" ]; then
    log "❌ Diretório de logs não encontrado em: $LOGS_DIR"
    exit 1
fi

# Calcular a data limite em segundos desde a época (epoch)
LIMIT_DATE_SEC=$(date -d "$DAYS days ago" +%s 2>/dev/null || date -v -"${DAYS}"d +%s 2>/dev/null)

if [ -z "$LIMIT_DATE_SEC" ]; then
    log "❌ Falha ao calcular a data limite."
    exit 1
fi

LIMIT_DATE_STR=$(date -d "@$LIMIT_DATE_SEC" "+%Y-%m-%d" 2>/dev/null || date -r "$LIMIT_DATE_SEC" "+%Y-%m-%d" 2>/dev/null)
log "📅 Logs anteriores a $LIMIT_DATE_STR serão removidos."

DELETED_COUNT=0

# Listar os subdiretórios que correspondem exatamente a YYYY-MM-DD
for dir_path in "$LOGS_DIR"/*; do
    if [ -d "$dir_path" ]; then
        dir_name=$(basename "$dir_path")
        
        # Verificar se o nome da pasta segue o padrão YYYY-MM-DD
        if [[ "$dir_name" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            # Converter a data da pasta para segundos
            dir_date_sec=$(date -d "$dir_name" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$dir_name" +%s 2>/dev/null)
            
            if [ -n "$dir_date_sec" ]; then
                if [ "$dir_date_sec" -lt "$LIMIT_DATE_SEC" ]; then
                    if [ "$DRY_RUN" = true ]; then
                        log "👉 [Simulação] Removendo: $dir_path (Data: $dir_name)"
                    else
                        log "🗑️ Removendo: $dir_path"
                        rm -rf "$dir_path"
                    fi
                    DELETED_COUNT=$((DELETED_COUNT + 1))
                fi
            fi
        fi
    fi
done

if [ "$DRY_RUN" = true ]; then
    log "✅ Simulação finalizada. Total de diretórios que seriam removidos: $DELETED_COUNT"
else
    log "✅ Limpeza finalizada com sucesso! Diretórios removidos: $DELETED_COUNT"
fi
