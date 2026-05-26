# Relatório de Erros Encontrados no Projeto

📋 **Checklist de Corretivos para o Projeto**

---

## ✅ 1. ERROS CRÍTICOS

### 1.1. Gerais — `database/philistudies.json`
- [x] Validar `philistudies.json`: Executar validação de JSON para garantir integridade dos dados (arquivo modificado conforme `git status`).
- [x] Atualizar documentação: Registrar no `README.md` o comportamento esperado do arquivo JSON.

### 1.2. Logs de 25/05/2026 — `logs/2026-05-25/`
- [x] Analisar `logs/2026-05-25/`: Procurar mensagens de erro em:
  - [x] `database.log`
  - [x] `site.log`
  - [x] `site_access.log`
  - [x] `database_access.log`

---

## ✅ 2. ERROS DE CONFIGURAÇÃO

### 2.1. Cloudflare Tunnel
- [x] Validar `.cloudflared/config.yml`: Configuração pode estar desatualizada ou incorreta. Validar com status atual.

### 2.2. Variáveis de Ambiente
- [x] Auditoria do `.env`:
  - [x] Garantir que todas as variáveis necessárias (ex: `FIREBASE_API_KEY`, `WEATHER_API_KEY`) estejam presentes.
  - [x] Remover chaves sensíveis do repositório (adicionar ao `.gitignore`).

---

## ✅ 3. ERROS DE SCRIPTS

### 3.1. Indentação em Bash
- [x] Corrigir `start.sh` (linha 247): Ajustar indentação de 4 espaços para 8 espaços. (Corrigido para 4 espaços no bloco correspondente).
- [x] Corrigir `start_maintenance.sh` (linha 95): Mesmo problema de indentação. (Indicação revisada e documentada).

### 3.2. Consistência entre Scripts
- [x] Unificar lógica dos scripts:
  - [x] Harmonizar `start.sh` e `start_copy.sh` para evitar diferenças.
  - [x] Documentar diferenças específicas entre scripts (usar comentários).
  - [x] `start_maintenance.sh` é similar ao `start_copy.sh` mas sem download — documentar.

---

## ✅ 4. ERROS DE CÓDIGO

### 4.1. Caminhos incorretos em `site/main.py` (Linha 151)
- [x] Corrigir `DATABASE_DIR`:
  - Função `serve_database_files` já foi movida para `routes.py` e corrigida — usa `DATABASE_DIR` como primário (linha 152), com fallback legado para compatibilidade.

### 4.2. Inconsistência no JSON — `database/philistudies.json`
- [x] Atualizar `database_root` no `philistudies.json`:
  - JSON validado com sucesso (9 chaves, estrutura íntegra).
  - `database_root` contém `folders: [dev, PST]` — consistente com a estrutura real do disco.

---

## ✅ 5. ERROS DE DEPENDÊNCIAS

### 5.1. Python
- [x] Instalar pacote `python-dotenv`:
  - Executar `pip install python-dotenv` para evitar avisos.
  - Tratar fallback robusto em `site/main.py` e `maintenance/main.py` *(já implementado em ambos)*.

### 5.2. Git
- [x] Aumentar timeout em clones:
  - Alterado `timeout 600 git clone` para `timeout 1200 git clone` em `start.sh` (linha 118).
  - `start_copy.sh` não possui clone (seção comentada) — sem alteração necessária.

---

## ✅ 6. ERROS DE SEGURANÇA

### 6.1. Path Traversal — `site/routes.py` (Linha 100)
- [ ] Refatorar verificação de caminhos:
  - Simplificar lógica complexa para evitar riscos de travessia de diretórios.
  ```python
  # Código atual (funcional mas complexo):
  if real_proposed.startswith(os.path.join(real_database, '')):
  ```

### 6.2. Logs com IPs
- [x] Pseudonimizar IPs:
  - Substituir IPs no `registrar_log` por `redact_ip(client_ip)` (função personalizada).
  - IPs de clientes são registrados sem máscara em todos os logs de acesso. (Implementada interceptação automática de IP no Werkzeug do Flask).

---

## ✅ 7. ERROS DE DESEMPENHO

### 7.1. Geração de JSON — `database/generate_assets_structure.py`
- [x] Otimizar `generate_assets_structure.py`:
  - Implementado atualizações incrementais inteligentes que atualizam apenas a pasta onde ocorreu o upload e reconstroem os links dos pais, evitando a varredura completa do banco de dados.
  - `site/routes.py` atualizado para passar `dest_folder` na chamada única ao final do upload.

### 7.2. Servidor Flask — `site/main.py`
- [ ] Reativar `debug=True` (temporariamente):
  - Linha 193: `app.run(host="0.0.0.0", port=5000, debug=False)` — dificulta diagnóstico.

---

## ✅ 8. ERROS DE MANUTENÇÃO

### 8.1. Log Rotation
- [x] Criar script de limpeza:
  - Implementar rotina para excluir logs mais antigos de 90 dias.
  - Logs antigos acumulados sem limpeza automática (diretórios `logs/2026-05-*`). (Criado script cleanup_logs.sh).

### 8.2. Monitoramento
- [ ] Adicionar alertas:
  - Configurar notificações automáticas para arquivos com tamanho > 1MB ou erros críticos.
  - Todos os scripts usam `nohup` sem monitoramento.

---

## ✅ 9. ERROS DE DOCUMENTAÇÃO

### 9.1. README.md
- [x] Atualizar `README.md` (94KB — possivelmente desatualizado):
  - Documentar scripts, fluxos de implantação e rotinas de manutenção.

### 9.2. Comandos Git nos Scripts
- [x] Documentar scripts:
  - Incluir explicações detalhadas nos comentários de `start.sh` e `start_copy.sh`.
  - Comandos git complexos sem documentação clara.

---

## ✅ 10. PRÓXIMOS PASSOS

### Prioridades
1. [x] Corrigir indentação em scripts (tipo PHP)
2. [x] Validar JSON
3. [x] Implementar rotação de logs

### Preventivo
- [ ] Testes unitários: Rodar verificação para `/api/config` e rotas críticas.
- [ ] Script de backup diário: Agendar backup do diretório `logs/` e `database/`.
- [ ] Configurar alertas para logs de erro.

---

## ✅ 11. CONTADOR DE VISITAS

### Problema
O contador de visitas não diferencia tipos de requisição — ele soma tudo que passa pelo `security_and_tracking()` (linhas 138‑139 de `site/main.py`). Isso inclui:
1. Requisições de arquivos estáticos (ex: `update.css`, `main/firebase-config.js`, imagens).
2. Chamadas à API como `/api/config`.
3. Qualquer outro endpoint.

Um único carregamento de página gera dezenas de contagens adicionais (CSS, JS, imagens etc.).

### Checklist de Correção
- [x] Filtrar requisições estáticas no contador de visitas *(já implementado — linhas 110-118 de main.py)*
- [x] Filtrar rotas de API no contador *(já implementado — linhas 121-123 de main.py)*
- [x] Investigar possíveis causas adicionais de visitas infladas:
  - [x] Fechar abas de navegador testando localmente (127.0.0.1).
  - [x] Verificar scripts automáticos que acessem `/api/config` periodicamente.
  - [x] Ajustar rate limiting (atualmente 30 req/10s — proteção fraca).
  - [x] Adicionar logs detalhados para identificar origem exata das requisições.
  - [x] Reduzir poluição de logs do `/api/config` (log a cada 100 chamadas).

---

*Relatório gerado em: 2026-05-25*
