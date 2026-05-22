# Checklist de Correções e Melhorias

## 1. Configuração e Segurança
- [x] Criar arquivo `.env` centralizado para todas as chaves de API do projeto.
- [x] Sincronizar Login: Implementada a geração de cookie `firebase_auth_token` para o backend.
- [x] Remover tokens hardcoded de scripts de inicialização (`setup.sh`, `start.sh`).

## 2. Arquitetura e Organização
- [x] Criada a pasta oculta `.system` para utilitários e lógica interna.
- [x] Criada a pasta `.temp` com subpastas `.repo` e `.zip` para histórico de downloads.
- [x] Centralização de Zipagem: Lógica movida para `.system/utils/zip_manager.py`.

## 3. Lógica e Performance
- [x] Otimizar upload de múltiplos arquivos no Database.
- [x] Corrigir lógica de caminhos no `generate_assets_structure.py`.
- [x] Expandir Calendário: Exibição e contagem de todos os 365 dias do ano.

## 4. Manutenção
- [x] Validar rotas e caminhos da pasta `maintenance` na raiz.
- [x] Corrigir servimento de Favicon e tratamento de erros nos logs.

---
*Status: Atualizado em 22/05/2026*
