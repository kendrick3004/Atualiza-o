# Diretrizes para Agentes de IA (AGENTS.md)

Este arquivo contém instruções e contextos essenciais para agentes de IA que operam neste repositório.

## 🚀 Visão Geral do Projeto
Este é um sistema full-stack que combina um site principal e um gerenciador de arquivos (Database), utilizando Flask no backend, Firebase para autenticação/sincronização e Cloudflare Tunnels para exposição segura.

## 🛠️ Regras de Operação
1.  **Preservação de Estrutura:** Não altere a estrutura de pastas sem autorização explícita. O projeto é dividido em `site/`, `database/` e `maintenance/`.
2.  **Autenticação:** Toda alteração no sistema de login deve respeitar a persistência de 7 dias e o gate de autenticação implementado em `auth-gate.js`.
3.  **Segurança (Rate Limiting):** O `rate-limiter.js` no frontend protege contra abusos, mas deve permitir operações legítimas de compactação (limite atual: 100 req/5s).
4.  **Infraestrutura:** O deploy utiliza dois túneis Cloudflare independentes. Verifique sempre o `setup_tunnels.sh` antes de mexer em serviços do sistema.

## 📂 Estrutura de Pastas Crítica
*   `/site/main.py`: Ponto de entrada do servidor Flask.
*   `/site/routes.py`: Definição de todas as rotas e lógica de backend.
*   `/site/database/`: Frontend do sistema de arquivos.
*   `/database/files/`: Local físico onde os arquivos do Database são armazenados.
*   `/maintenance/`: Páginas de erro (404, 429, 500) e modo manutenção.

## 📝 Notas de Desenvolvimento
*   Sempre atualize o `philistudies.json` ao adicionar ou remover arquivos manualmente no servidor usando o script `generate_assets_structure.py`.
*   A responsividade mobile deve ser testada especialmente na faixa de 1024px-1028px.

IMPORTANTE: Sempre atualizar o README.md, com cada implemnetação que foi posto e arumado e tal.

<!-- README.md — Documentação Completa do Projeto -->
<!-- Última atualização: 2026-05-14 -->
