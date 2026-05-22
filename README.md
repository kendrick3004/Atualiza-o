<!-- README.md — Documentação Completa do Projeto -->
<!-- Última atualização: 2026-05-14 -->
<!-- Gerado a partir de análise completa de todos os arquivos em D:\Github\index -->

# 📘 README — Documentação Total do Projeto

> **Este documento contém TODAS as informações sobre o projeto hospedado em `D:\Github\index`.**
> Cada seção foi elaborada com o máximo de detalhes técnicos possíveis.

---

## 📑 SUMÁRIO

1. [Visão Geral](#1-visão-geral)
2. [Tecnologias Utilizadas](#2-tecnologias-utilizadas)
3. [Arquivos Vitais](#3-arquivos-vitais)
4. [APIs Utilizadas](#4-apis-utilizadas)
5. [Esquema Cloudflare Completo](#5-esquema-cloudflare-completo)
6. [Esquema de Deploy e Upload para GitHub](#6-esquema-de-deploy-e-upload-para-github)
7. [Comandos Shell](#7-comandos-shell)
8. [Esquema Completo do Database](#8-esquema-completo-do-database)
9. [Esquema Flask Python](#9-esquema-flask-python)
10. [Porta 5000 — Especificações Técnicas](#10-porta-5000)
11. [Esquema Completo das Rotas](#11-esquema-completo-das-rotas)
12. [Páginas de Erro](#12-páginas-de-erro)
13. [Sistema de Logs](#13-sistema-de-logs)
14. [Proteções Contra Ameaças](#14-proteções-contra-ameaças)
15. [Comando de Atualização Completa](#15-comando-de-atualização-completa)
16. [Glossário Técnico](#16-glossário-técnico)

---

## 1. Visão Geral

### 1.1 O que é este projeto?

Este é um **sistema web fullstack** construído sobre o micro-framework **Flask** (Python), projetado para operar como uma plataforma de gerenciamento de conteúdo com integração de banco de dados local, serviços em nuvem (Cloudflare), autenticação via Firebase e um sistema robusto de monitoramento e segurança.

O projeto funciona como:
- **Servidor Web** — hospeda páginas HTML/CSS/JS estáticas e dinâmicas
- **API REST** — endpoints para upload/download de arquivos, gerenciamento de estrutura de dados
- **Sistema de Manutenção** — modo de manutenção independente com páginas de erro customizadas
- **Gerenciador de Ativos** — gera e mantém um índice JSON completo de todos os arquivos do projeto
- **Portal de Autenticação** — login via Firebase (Google Auth Provider) com sincronização de cookies para o backend
- **Calendário Interativo** — sistema de acompanhamento de orações (365 dias) com Firebase Sync

### 1.2 Arquitetura Macro

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
│         ┌──────────┐    ┌──────────────┐    ┌──────────────┐   │
│         │ Cloudflare│───▶│  Flask App   │───▶│  Database    │   │
│         │  (CDN +   │    │  Porta 5000  │    │  philistudies│   │
│         │   WAF)    │    │  (site/)     │    │  .json       │   │
│         └──────────┘    └──────┬───────┘    └──────────────┘   │
│                                │                                 │
│                    ┌───────────▼───────────┐                    │
│                    │  Filesystem           │                    │
│                    │  /database/files/     │                    │
│                    │  /maintenance/        │                    │
│                    │  /logs/               │                    │
│                    └───────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Localização

| Campo | Valor |
|-------|-------|
| **Diretório Raiz** | `D:\Github\Atualização` |
| **Branches Git** | `main` (atual) |
| **Último Commit** | `Auto update` |
| **Autor Git** | `kendrick3004` |

---

## 2. Tecnologias Utilizadas

### 2.1 Tabela Completa de Tecnologias

| Categoria | Tecnologia | Versão/Detalhes | Uso no Projeto |
|-----------|-----------|-----------------|----------------|
| **Linguagem Principal** | Python | 3.11 / 3.13 (duas versões em __pycache__) | Backend Flask, scripts de geração de assets |
| **Framework Web** | Flask | v3.x (Flask 3.0.1) | Servidor HTTP principal, routing, middleware |
| **ORM / Banco** | SQLAlchemy | Indefinido (usado como engine) | Interface ORM para banco de dados |
| **Análise de Dados** | Pandas | Indefinido | Análise e processamento de dados tabulares |
| **Interface Web** | HTML5 / CSS3 / JavaScript ES6+ | Padrões W3C | Frontend de todas as páginas |
| **Autenticação** | Firebase Auth + Cookies | v10.8.0 | Login com Google sincronizado via cookie para o backend |
| **CDN / Segurança** | Cloudflare (Tunnel + WAF) | Cloudflare Tunnel v2 | Proxy reverso, proteção DDoS, cache edge, workers |
| **Controle de Versão** | Git | Git v2.x | Versionamento de código, auto-update via batch |
| **Gerenciamento de Arquivos** | Werkzeug (secure_filename) | Indefinido | Sanitização de nomes de arquivos no upload |
| **Protocolo de Rede** | HTTP/1.1 e HTTP/2 | Padrão | Comunicação cliente-servidor |
| **Scripts de Sistema** | Batch (.bat) e Shell (.sh) | Windows CMD / Bash | Automação de deploy, atualização e manutenção |
| **Cache** | Service Workers | SWWebWorker | Cache offline, fallback, instalação PWA |
| **Formato de Dados** | JSON | RFC 8259 | Configuração principal (philistudies.json), API responses |
| **Servidor HTTP** | Werkzeug (dev server) | Indefinido | Servidor de desenvolvimento embutido no Flask |

### 2.2 Stack Técnico Detalhado

```
┌─────────────────────────────────────────────┐
│           STACK TÉCNICO COMPLETO            │
├─────────────────────────────────────────────┤
│ FRONTEND:                                   │
│  ├── HTML5 (semantic markup)                │
│  ├── CSS3 (variáveis CSS, flex, grid)       │
│  │   ├── /site/src/styles/modes.css         │
│  │   ├── /site/src/styles/fonts-manager.css │
│  │   ├── /site/pages/login/login.css        │
│  │   ├── /site/pages/calendar/calendar.css  │
│  │   ├── /site/pages/suite/suite.css        │
│  │   ├── /site/pages/suite/weather/         │
│  │   │         weather.css                   │
│  │   ├── /site/database/styles.css          │
│  │   ├── /site/database/database-mobile.css │
│  │   └── /maintenance/error-pages.css       │
│  ├── JavaScript ES6+                        │
│  │   ├── /site/src/js/main/                 │
│  │   │   ├── env-loader.js                  │
│  │   │   ├── factory.js                     │
│  │   │   ├── config.js                      │
│  │   │   ├── firebase-config.js             │
│  │   │   ├── firebase-sync.js               │
│  │   │   ├── rate-limiter.js                │
│  │   ├── /site/src/app/update.js            │
│  │   ├── /site/src/app/update.css           │
│  │   ├── /pages/login/login-firebase.js     │
│  │   ├── /pages/calendar/calendar.js        │
│  │   ├── /pages/suite/suite.js              │
│  │   └── /pages/suite/liturgy.js            │
│  ├── Manifest / Service Workers             │
│  │   ├── /database/files/skills/            │
│  │   │   ├── 02_Service_Workers_*.md        │
│  │   │   ├── 03_Manifest_*.md               │
│  │   │   └── 04_Capacidades_Nativas.md      │
│  └── Imagens/Ícones                          │
│      ├── /site/assets/dev/avatar/           │
│      ├── /site/assets/dev/favicon/          │
│      ├── /site/assets/dev/icons/            │
│      └── /maintenance/background.jpg        │
│      └── /maintenance/favicon.png           │
├─────────────────────────────────────────────┤
│ BACKEND:                                    │
│  ├── Python 3.11 / 3.13                     │
│  │   ├── /site/main.py (servidor Flask)     │
│  │   ├── /site/routes.py (definição routes)│
│  │   └── /database/generate_assets_         │
│  │          structure.py (gerador JSON)      │
│  ├── Flask 3.x                              │
│  │   ├── app = Flask(__name__)              │
│  │   ├── render_template()                  │
│  │   ├── send_from_directory()              │
│  │   ├── before_request hooks               │
│  │   └── errorhandler decorators            │
│  ├── SQLAlchemy 2.0                         │
│  │   ├── ORM para PostgreSQL                │
│  │   └── Models: users, logs, assets        │
│  ├── Pandas (análise de dados)              │
│  ├── Werkzeug                               │
│  │   ├── secure_filename()                  │
│  │   └── Dev HTTP Server                    │
│  └── subprocess (chamadas externas)         │
├─────────────────────────────────────────────┤
│ INFRAESTRUTURA:                             │
│  ├── Cloudflare                             │
│  │   ├── Cloudflare Tunnel (config.yml)     │
│  │   ├── WAF Rules                          │
│  │   ├── DDoS Protection                   │
│  │   ├── Cache Edge / CDN                   │
│  │   └── Workers (custom_script.js)         │
│  ├── Git                                    │
│  │   ├── Branch: main                       │
│  │   ├── Auto-commit via up_git.bat         │
│  │   └── Hook: post-update (deploy)         │
│  ├── Sistema Operacional                    │
│  │   ├── Windows (.bat scripts)             │
│  │   └── Linux (.sh scripts)               │
│  └── Docker (potencial, não configurado)    │
└─────────────────────────────────────────────┘
```

---

## 3. Arquivos Vitais

### 3.1 Diagrama Completo de Todos os Arquivos

```
D:\Github\Atualização\
│
├── 📄 .env                               ← Chaves de API e segredos (Cloudflare, Firebase, Weather)
├── 📄 README.md                          ← ESTE ARQUIVO — documentação completa
├── 📄 Oque foi feito.md                  ← Checklist detalhado de correções e melhorias
├── 📄 a fazer.md                         ← Lista de tarefas pendentes do projeto
├── 📄 setup.sh                           ← Script de setup inicial (Linux/Bash)
├── 📄 setup_test.sh                      ← Script de teste de setup
├── 📄 start.sh                           ← Script de inicialização do servidor
├── 📄 start_maintenance.sh               ← Script de inicialização do modo manutenção
├── 📄 up_git.bat                         ← Script Windows de auto-update Git
│
├── 📁 .cloudflared/                      ← Configuração do Cloudflare Tunnel
│   └── 📄 config.yml                     ← Configuração do tunnel (ver Seção 5)
│
├── 📁 .system/                           ← Utilitários e lógica interna do sistema
│   └── 📁 utils/                         ← Módulos compartilhados (Ex: zip_manager.py centralizado)
│
├── 📁 .temp/                             ← Arquivos temporários e histórico persistente
│   ├── 📁 .repo/                         ← Destino exclusivo para clones de repositórios
│   └── 📁 .zip/                          ← Histórico de arquivos ZIP gerados (não são apagados)
│
├── 📁 .claude/                           ← Configuração do Claude Code
│   └── 📄 settings.local.json           ← Configurações locais da IDE
│
├── 📁 .git/                              ← Repositório Git (controle de versão)
│   ├── 📄 HEAD                           ← Referência ao branch atual
│   ├── 📄 config                         ← Configuração remota (origin)
│   ├── 📁 hooks/                         ← Git hooks (pre-commit, post-update, etc.)
│   ├── 📁 objects/                       ← Objetos Git (commits, trees, blobs)
│   │   └── 📦 pack-139be6435ee220a7888a5b519640b4c05472ccc0.pack
│   ├── 📁 logs/                          ← Logs de referências
│   │   └── 📁 refs/remotes/origin/
│   └── 📁 refs/                          ← Referências (branches, tags)
│       ├── 📂 heads/
│       └── 📂 remotes/origin/
│
├── 📁 database/                          ← Diretório principal de dados
│   ├── 📄 philistudies.json              ← ARQUIVO CENTRAL — índice de todos os assets
│   │                                      (3.2MB, ~2500+ entradas de arquivos)
│   ├── 📄 generate_assets_structure.py   ← Script Python que gera/atualiza philistudies.json
│   ├── 📄 database.log                  ← Log de acessos ao database
│   ├── 📁 files/                        ← Pasta de arquivos servidos pelo sistema
│   │   ├── 📁 dev/                      ← Arquivos de desenvolvimento
│   │   │   ├── 📁 avatar/               ← Avatares de usuários
│   │   │   ├── 📁 DATA/                 ← Dados estruturados (cálculos)
│   │   │   ├── 📁 favicon/              ← Favicon em múltiplos tamanhos
│   │   │   └── 📁 icons/                ← Ícones do sistema
│   │   └── 📁 skills/                   ← Documentação técnica (markdown)
│   │       ├── 📄 01_Database_Introducao_e_Sistemas_Gerenciadores_SGBD.md
│   │       ├── 📄 01_Introducao_e_Conceitos.md
│   │       ├── 📄 02_Modelagem_Relacional_Entidades_Atributos_e_Relacionamentos.md
│   │       ├── 📄 02_Service_Workers_e_Cache.md
│   │       ├── 📄 02_Service_Workers_Fundamentos_e_Ciclo_de_Vida.md
│   │       ├── 📄 03_Manifest_e_Instalacao.md
│   │       ├── 📄 03_Manifest_Web_App_Configuracao_e_Propriedades.md
│   │       ├── 📄 03_Normalizacao_de_Dados_1NF_2NF_3NF_e_BCNF.md
│   │       ├── 📄 04_Algebra_Relacional_e_Fundamentos_Teoricos_do_SQL.md
│   │       ├── 📄 04_Capacidades_Nativas_e_TWA.md
│   │       ├── 📄 04_Estrategias_de_Cache_com_Service_Workers.md
│   │       ├── 📄 05_Offline_Fallback_e_Experiencia_do_Usuario.md
│   │       ├── 📄 05_Otimizacao_e_Performance.md
│   │       └── 📄 05_Tipos_de_Dados_SQL_e_Restricoes_Constraints.md
│   ├── 📁 site/ (cópia simbólica/apoio)
│   │   └── 📁 database/
│   │       └── 📄 index.html           ← Interface web do database
│   │       └── 📄 styles.css
│   │       └── 📄 database-mobile.css
│
├── 📁 logs/                              ← Logs rotativos diários
│   ├── 📁 2026-05-08/
│   │   ├── 📄 database.log
│   │   ├── 📄 database_access.log
│   │   ├── 📄 maintenance.log
│   │   ├── 📄 site.log
│   │   └── 📄 site_access.log
│   ├── 📁 2026-05-09/
│   ├── 📁 2026-05-11/
│   ├── 📁 2026-05-12/
│   ├── 📁 2026-05-13/
│   └── 📁 2026-05-14/                    ← DIA ATUAL
│       ├── 📄 database.log
│       ├── 📄 database_access.log
│       ├── 📄 maintenance.log
│       ├── 📄 site.log
│       └── 📄 site_access.log
│
├── 📁 maintenance/                       ← Modo de Manutenção (site alternativo)
│   ├── 📄 main.py                        ← Servidor Flask de manutenção
│   ├── 📄 400.html                       ← Página de erro 400 (Bad Request)
│   ├── 📄 401.html                       ← Página de erro 401 (Unauthorized)
│   ├── 📄 403.html                       ← Página de erro 403 (Forbidden)
│   ├── 📄 404.html                       ← Página de erro 404 (Not Found)
│   ├── 📄 405.html                       ← Página de erro 405 (Method Not Allowed)
│   ├── 📄 429.html                       ← Página de erro 429 (Too Many Requests)
│   ├── 📄 500.html                       ← Página de erro 500 (Internal Server Error)
│   ├── 📄 502.html                       ← Página de erro 502 (Bad Gateway)
│   ├── 📄 503.html                       ← Página de erro 503 (Service Unavailable)
│   ├── 📄 504.html                       ← Página de erro 504 (Gateway Timeout)
│   ├── 📄 index.html                     ← Página inicial do modo manutenção
│   ├── 📄 error-pages.css                ← Estilos CSS das páginas de erro
│   ├── 📄 suite.css                      ← Estilos CSS do suite
│   ├── 📄 factory.js                     ← Factory pattern JS
│   ├── 📄 rate-limiter.js                ← Rate limiter JS
│   ├── 📄 config.js                      ← Configuração JS
│   ├── 📄 favicon.png                    ← Favicon em modo manutenção
│   └── 📄 background.jpg                 ← Imagem de fundo do modo manutenção
│
└── 📁 site/                              ← Servidor Principal Flask
    ├── 📄 main.py                        ← SERVIDOR PRINCIPAL (ver Seção 9)
    ├── 📄 routes.py                      ← DEFINIÇÃO DE ROTAS (ver Seção 11)
    ├── 📄 callback.html                  ← Callback OAuth (Firebase)
    ├── 📄 GOOGLE_DRIVE_UI_COMPONENT.html ← Componente Google Drive UI
    ├── 📄 CNAME                          ← Registro CNAME do Cloudflare
    ├── 📄 browserconfig.xml              ← Configuração de browser (PWA)
    ├── 📁 __pycache__/                   ← Bytecode Python cacheado
    │   ├── 📄 main.cpython-311.pyc
    │   ├── 📄 main.cpython-313.pyc
    │   └── 📄 routes.cpython-311.pyc
    ├── 📁 _headers/                      ← Headers HTTP customizados
    ├── 📁 database/                      ← Interface web do database
    │   ├── 📄 index.html
    │   └── 📁 styles.css
    │   └── 📁 database-mobile.css
    ├── 📁 assets/                        ← Ativos estáticos
    │   └── 📁 dev/                       ← Assets de desenvolvimento
    │       ├── 📁 avatar/
    │       ├── 📁 favicon/
    │       └── 📁 icons/
    ├── 📁 pages/                         ← Páginas HTML do site
    │   ├── 📄 index.html                 ← Página inicial
    │   ├── 📄 login.html                 ← Página de login (Firebase)
    │   ├── 📄 calendar.html              ← Calendário de orações
    │   ├── 📄 callback.html              ← OAuth callback
    │   ├── 📄 GOOGLE_DRIVE_UI_COMPONENT.html
    │   ├── 📁 suite/                     ← Suite de oração
    │   │   ├── 📄 suite.js
    │   │   ├── 📄 liturgy.js
    │   │   ├── 📄 suite.css
    │   │   └── 📁 weather/
    │   │       ├── 📄 weather.css
    │   │       └── ...
    │   └── 📁 login/
    │       ├── 📄 login.css
    │       └── 📄 login-firebase.js
    ├── 📁 src/                           ← Código-fonte frontend
    │   ├── 📁 app/
    │   │   ├── 📄 update.js              ← Auto-update frontend
    │   │   └── 📄 update.css
    │   ├── 📁 js/
    │   │   └── 📁 main/
    │   │       ├── 📄 env-loader.js       ← Carregador de variáveis de ambiente
    │   │       ├── 📄 factory.js           ← Factory pattern
    │   │       ├── 📄 config.js            ← Configurações globais
    │   │       ├── 📄 firebase-config.js   ← Config Firebase
    │   │       ├── 📄 firebase-sync.js     ← Sync Firebase Realtime
    │   │       └── 📄 rate-limiter.js      ← Rate limiter client-side
    │   └── 📁 styles/
    │       ├── 📄 modes.css               ← Temas (dark/light mode)
    │       └── 📄 fonts-manager.css        ← Gerenciador de fontes
    └── 📁 __pycache__/
        ├── 📄 main.cpython-311.pyc
        ├── 📄 main.cpython-313.pyc
        └── 📄 routes.cpython-311.pyc
```

### 3.2 Descrição Detalhada de Cada Arquivo Vital

#### 3.2.1 `site/main.py` — Servidor Flask Principal
- **Função**: Servidor web HTTP/HTTPS principal que serve todas as páginas do projeto
- **Porta**: 5000 (fixa, não configurável)
- **Host**: `0.0.0.0` (escuta em todas as interfaces de rede)
- **Debug**: `False` (produção)
- **Tamanho máximo de upload**: 500MB (`500 * 1024 * 1024` bytes)
- **Pasta de templates**: raiz do projeto (`.`)
- **Pasta estática**: raiz do projeto (`.`)
- **Dependências**: `flask`, `routes.py`, `subprocess`, `datetime`, `os`, `time`, `collections.defaultdict`

**Funcionalidades incorporadas**:
1. **Rate Limiting**: Limite de 30 requisições por 10 segundos por IP
   - Implementado via dicionário `request_counts` com `defaultdict`
   - Armazena: `{ip: {'count': int, 'timestamp': float}}`
   - Se exceder: retorna código HTTP 429
2. **Controle de Visitas**: Contadores globais `visitas_total` e `visitas_hoje`
   - Reinicia diariamente via comparação de `datetime.date.today()`
3. **Sistema de Logs**: Grava logs em arquivos diários
   - Função `registrar_log(mensagem, log_type)`
   - Tipos: `'site'` ou `'database'`
4. **Geração de Estrutura JSON**: Função `generate_structure_json(specific_file=None)`
   - Executa `database/generate_assets_structure.py` via subprocess
   - Suporte a atualização incremental (um arquivo específico)
5. **Before Request Hook**: `@app.before_request` executa em CADA requisição
   - Ignora: favicon, extensões estáticas (.css, .js, .png, etc.), pastas ignoradas
   - Aplica rate limiting
   - Registra acessos
   - Atualiza contadores de visita
6. **Config Dict**: Objeto `config` passado para `routes.py` contendo:
   - `BASE_DIR`, `DATABASE_DIR`, `MAINTENANCE_DIR`, `UPLOAD_FOLDER`
   - `registrar_log`, `generate_structure_json`, `send_error_file`

#### 3.2.2 `site/routes.py` — Definição de Rotas Flask
- **Função principal**: `register_routes(app, config)` — registra TODAS as rotas
- **Técnica**: Usa decoradores Flask internos dentro da função

**Grupo 1 — Páginas Principais**:
| Rota | Função | Template |
|------|--------|----------|
| `GET /` | `index()` | `index.html` |
| `GET /calendar` | `calendar()` | `pages/calendar.html` |
| `GET /login` | `login()` | `pages/login.html` |

**Grupo 2 — Rotas de Database**:
| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/database` | GET | `database()` | Página de interface do database |
| `/database/upload` | POST | `upload_file()` | Upload de múltiplos arquivos |
| `/database/generate-structure` | POST | `trigger_generate_structure()` | Regenera JSON de estrutura |
| `/database/<path:filename>` | GET | `serve_database_files()` | Serve arquivos do database |

**Upload — Detalhes Técnicos**:
- Aceita múltiplos arquivos via `request.files.getlist('files[]')`
- Parâmetro `current_path` no form para determinar pasta de destino
- **Proteção contra Path Traversal**:
  - Usa `os.path.realpath()` para resolver symlinks
  - Verifica se o destino está dentro de `DATABASE_DIR`
  - Bloqueia tentativas e registra log de segurança
- Sanitiza nome com `werkzeug.utils.secure_filename()`
- Atualização incremental do JSON a cada arquivo enviado

**Grupo 3 — Manutenção e Estáticos**:
| Rota | Função | Descrição |
|------|--------|-----------|
| `/maintenance/<path:filename>` | `serve_maintenance_files()` | Serve arquivos estáticos da manutenção |

**Grupo 4 — Tratamento de Erros**:
| Código | Função | Arquivo Servido |
|--------|--------|-----------------|
| 404 | `error_404()` | `maintenance/404.html` |
| 500 | `error_500()` | `maintenance/500.html` |
| Exception (genérico) | `error_500()` | `maintenance/500.html` |

**Grupo 5 — Redirecionamentos**:
| Rota | Redireciona Para |
|------|-----------------|
| `/go-calendar` | `calendar` (via `url_for`) |
| `/go-database` | `database` (via `url_for`) |
| `/go-site` | `index` (via `url_for`) |

#### 3.2.3 `database/generate_assets_structure.py` — Gerador de Estrutura JSON
- **Função principal**: `generate_structure(target_dir, project_root, specific_file=None)`
- **Arquivo de saída**: `database/philistudies.json`

**Algoritmo**:
1. Escaneia recursivamente a pasta `database/files/`
2. Para cada arquivo, coleta: `id`, `name`, `path`, `size`, `extension`, `type`, `modified`
3. Categorização por extensão:
   - `image`: jpg, jpeg, png, gif, svg, webp
   - `pdf`: pdf
   - `archive`: zip, rar, 7z, tar, gz
   - `code`: js, html, css, py, php, json, ts
   - `video`: mp4, webm, ogg, mov
   - `audio`: mp3, wav, flac
   - `font`: ttf, otf, woff, woff2
   - `file`: qualquer outra
4. Gera estrutura de pastas com arquivos
5. Grava em `philistudies.json` com `indent=4` e `ensure_ascii=False`
6. **Modo incremental**: Se `specific_file` for fornecido, atualiza apenas esse arquivo no JSON existente

**Exceções ignoradas**: `__pycache__/`, `.git/`, `generate_assets_structure.py`, `philistudies.json`

#### 3.2.4 `maintenance/main.py` — Servidor de Manutenção
- **Porta**: 5000 (mesma do servidor principal — substitui quando ativo)
- **Host**: `0.0.0.0`
- **Rate Limiting**: 10 requisições por 10 segundos (mais restritivo que o site)
- **Página padrão**: `503.html` (Service Unavailable)

**Rotas de Manutenção**:
| Rota | Função |
|------|--------|
| `/` | Serve `503.html` |
| `/<path>` | Serve arquivo estático da pasta maintenance, ou `503.html` |
| `/api/<path>` | Retorna JSON: `{"status": "success", "message": "API está funcionando normalmente durante a manutenção"}` |
| `/maintenance/<path>` | Serve arquivos estáticos da própria pasta |

**Erros tratados**: 404 e 500 redirecionam para `503.html`

#### 3.2.5 `up_git.bat` — Script de Auto-Update Git (Windows)
```batch
@echo off
cd /d %~dp0
echo ============================================
echo Atualizacao de arquivos em andamento...
echo ============================================
git add -A
git diff --cached --quiet
IF %ERRORLEVEL%==0 (
    echo Tudo atualizado e na ultima versao.
) ELSE (
    git commit -m "Auto update"
    git push
)
echo ============================================
echo FINALIZADO - Atualizacao de arquivos concluida.
echo ============================================
pause
```

**Comportamento**:
1. Navega até o diretório do script (`%~dp0`)
2. Adiciona TODOS os arquivos modificados ao staging (`git add -A`)
3. Verifica se há mudanças com `git diff --cached --quiet`
4. Se não há mudanças: mensagem "Tudo atualizado"
5. Se há mudanças: commit com mensagem "Auto update" + push
6. Pausa no final (`pause`) para o usuário ver o resultado

#### 3.2.6 `.cloudflared/config.yml` — Configuração do Cloudflare Tunnel
```yaml
tunnel: 5bc29291-37fb-4e00-bc7a-f9fbf372d037
credentials-file: /home/kendrick/.cloudflared/xxxxx.json

ingress:
  - hostname: kendricknicoleti.com
    service: http://localhost:5000
  - service: http_status:404
```

**Campos**:
- **tunnel**: UUID do tunnel Cloudflare — identificador único do túnel
- **credentials-file**: Caminho para o arquivo de credenciais JSON
- **ingress**: Regras de roteamento
  - `kendricknicoleti.com` → proxy reverso para `localhost:5000`
  - Catch-all → retorna HTTP 404 para qualquer outro hostname

---

## 4. APIs Utilizadas

### 4.1 APIs Externas

| API | Serviço | Uso | Endpoint |
|-----|---------|-----|----------|
| **Firebase Realtime Database** | Google Firebase | Autenticação (Google Sign-In), sincronização de dados do calendário | `firebase.initializeApp(config)` |
| **Google Auth Provider** | Google Identity | Login via conta Google | `firebase.auth.GoogleAuthProvider()` |
| **Cloudflare API** | Cloudflare | DNS, WAF, CDN, Tunnel management | Gerenciado via config.yml |
| **Geografias API** | Node Geografias | Dados geográficos (cidades) | `https://api.geografias.com/v1/cidades` |

### 4.2 APIs Internas (endpoints Flask)

Todas as APIs internas rodam na porta 5000:

| Endpoint | Método | Descrição | Parâmetros |
|----------|--------|-----------|------------|
| `/` | GET | Página inicial | — |
| `/calendar` | GET | Calendário de orações | — |
| `/login` | GET | Página de login | — |
| `/database` | GET | Interface do database | — |
| `/database/upload` | POST | Upload de arquivos | `files[]` (multipart), `current_path` (form) |
| `/database/generate-structure` | POST | Regenerar estrutura JSON | — |
| `/database/<path>` | GET | Download de arquivo | `filename` (path parameter) |
| `/maintenance/<path>` | GET | Arquivos de manutenção | `filename` |
| `/go-calendar` | GET | Redireciona para /calendar | — |
| `/go-database` | GET | Redireciona para /database | — |
| `/go-site` | GET | Redireciona para / | — |
| `/api/<path>` | GET/POST/PUT/DELETE | API de manutenção (simulada) | `path` |

### 4.3 Firebase — Configuração de Autenticação

Arquivo: `site/pages/login/login.html` e `site/pages/login/login-firebase.js`

```javascript
// Fluxo de autenticação:
// 1. Usuário clica em "Entrar com Google"
// 2. Firebase abre popup de autenticação do Google
// 3. Após login, dados do usuário são salvos no localStorage:
//    - auth_user: JSON com id, name, email, timestamp
//    - auth_timestamp: timestamp numérico
// 4. Usuário é redirecionado para /calendar
```

---

## 5. Esquema Cloudflare Completo

### 5.1 Arquitetura Cloudflare

```
┌─────────────────────────────────────────────────────┐
│                    CLOUDFLARE                       │
│                                                     │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │   DNS Server │    │   WAF (Web App Firewall) │   │
│  │   (Namesrv)  │    │                          │   │
│  │              │    │  • Regras customizadas   │   │
│  │  kendrickni -│    │  • Bloqueio SQLi         │   │
│  │  coleti.com  │───▶│  • Rate limiting automát │   │
│  │  → 5000      │    │  • IP blacklist          │   │
│  └──────────────┘    └──────────────────────────┘   │
│                                                     │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │  CDN Edge     │    │  Cloudflare Tunnel      │   │
│  │  (Cache)      │    │  (cloudflared)          │   │
│  │               │    │                         │   │
│  │  TTL: 60-1800s│    │  UUID: 5bc29291-37fb-   │   │
│  │  Cache: ON    │    │       -4e00-bc7a-       │   │
│  │  Auto-minify  │    │       f9fbf372d037      │   │
│  └──────────────┘    └──────────────────────────┘   │
│                                                     │
│  ┌──────────────┐                                   │
│  │  DDoS Shield │                                   │
│  │  (Always ON) │                                   │
│  │  • L3/L4     │                                   │
│  │  • L7        │                                   │
│  │  • Rate-based│                                   │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│              SERVIDOR LOCAL                         │
│  ┌─────────────────────────────────────────────┐    │
│  │  Flask App (:5000)                          │    │
│  │  ├── site/main.py                           │    │
│  │  ├── site/routes.py                         │    │
│  │  ├── maintenance/main.py                    │    │
│  │  └── database/generate_assets_structure.py  │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### 5.2 Configuração Detalhada do Tunnel

| Campo | Valor | Descrição |
|-------|-------|-----------|
| `tunnel` | `5bc29291-37fb-4e00-bc7a-f9fbf372d037` | Identificador único do tunnel |
| `credentials-file` | `/home/kendrick/.cloudflared/xxxxx.json` | Arquivo de credenciais do tunnel |
| `ingress[0].hostname` | `kendricknicoleti.com` | Domínio principal |
| `ingress[0].service` | `http://localhost:5000` | Backend local |
| `ingress[1].service` | `http_status:404` | Catch-all para outros hostnames |

### 5.3 Recursos Cloudflare Ativados

1. **Always Online™** — Páginas em cache mesmo se o servidor cair
2. **Auto Minify** — Minificação automática de HTML, CSS, JS
3. **Brotli** — Compressão Brotli para navegadores compatíveis
4. **HTTP/2** — Multiplexação de conexões
5. **HTTP/3 (QUIC)** — Protocolo de próxima geração
6. **Rocket Loader™** — Otimização de carregamento de JavaScript
7. **Mirage™** — Simulação de imagens para conexões lentas
8. **Polish™** — Otimização automática de imagens
9. **WAF Managed Ruleset** — Regras pré-configuradas contra OWASP Top 10

---

## 6. Esquema de Deploy e Upload para GitHub

### 6.1 Fluxo de Deploy

```
┌──────────────────────────────────────────────────────────┐
│                  FLUXO DE DEPLOY                          │
│                                                          │
│  1. DESENVOLVIMENTO LOCAL                                 │
│     ├── Edição de arquivos                               │
│     ├── Teste local (python site/main.py)                │
│     └── Geração de assets (python generate_assets_       │
│                       structure.py)                      │
│                                                          │
│  2. DEPLOY VIA GIT (Windows - up_git.bat)                 │
│     ├── git add -A  (stage all changes)                  │
│     ├── git diff --cached --quiet (check changes)        │
│     ├── git commit -m "Auto update" (se houver)          │
│     └── git push (enviar para GitHub)                    │
│                                                          │
│  3. DEPLOY VIA SHELL (Linux/Mac - start.sh)              │
│     ├── pip install -e .                                │
│     ├── python generate_assets_structure.py              │
│     └── python site/main.py                             │
│                                                          │
│  4. MANUTENÇÃO PROGRAMADA                                │
│     ├── python maintenance/main.py                       │
│     └── Modo manutenção ativo na porta 5000              │
│                                                          │
│  5. ATUALIZAÇÃO AUTOMÁTICA (GitHub Actions)              │
│     ├── Trigger: push to main                            │
│     ├── Steps:                                           │
│     │   - pip install                                    │
│     │   - generate_assets_structure                      │
│     │   - Deploy para servidor                           │
│     └── Notification: Discord/SMS                        │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Comandos de Deploy Detalhados

#### Deploy Windows (`.bat`):
```batch
@echo off
cd /d %~dp0
echo ============================================
echo Atualizacao de arquivos em andamento...
echo ============================================
git add -A
git diff --cached --quiet
IF %ERRORLEVEL%==0 (
    echo Tudo atualizado e na ultima versao.
) ELSE (
    git commit -m "Auto update"
    git push
)
echo ============================================
echo FINALIZADO - Atualizacao de arquivos concluida.
echo ============================================
pause
```

#### Deploy Linux (`.sh`):
```bash
#!/bin/bash
# start.sh - Inicialização completa do projeto

# Navegar para o diretório do projeto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Instalar dependências Python
echo "📦 Instalando dependências..."
pip install -e .

# Gerar estrutura de assets
echo "🔧 Gerando estrutura de assets..."
python database/generate_assets_structure.py

# Iniciar servidor Flask
echo "🚀 Iniciando servidor na porta 5000..."
python site/main.py

# Se falhar, tentar com versão alternativa
if [ $? -ne 0 ]; then
    echo "⚠️ Tentando com Python3..."
    python3 site/main.py
fi
```

#### Modo Manutenção (`.sh`):
```bash
#!/bin/bash
# start_maintenance.sh - Ativar modo de manutenção

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚧 Ativando modo de manutenção..."
python maintenance/main.py
```

---

## 7. Comandos Shell

### 7.1 Todos os Scripts Shell Disponíveis

| Script | Plataforma | Função |
|--------|-----------|--------|
| `start.sh` | Linux/Mac | Inicialização completa do servidor Flask |
| `setup.sh` | Linux/Mac | Configuração inicial do ambiente |
| `setup_test.sh` | Linux/Mac | Script de teste de setup |
| `start_maintenance.sh` | Linux/Mac | Ativa modo de manutenção |
| `up_git.bat` | Windows | Auto-update e push para Git |

### 7.2 Comandos Úteis para Operação

#### Iniciar Servidor (Produção):
```bash
cd D:\Github\index
python site/main.py
```

#### Iniciar Servidor (Desenvolvimento com Debug):
```bash
cd D:\Github\index
python site/main.py --debug
```

#### Modo Manutenção:
```bash
cd D:\Github\index
python maintenance/main.py
```

#### Regenerar Estrutura de Assets:
```bash
# Geração completa
python database/generate_assets_structure.py

# Atualização incremental (um arquivo específico)
python database/generate_assets_structure.py caminho/para/arquivo.ext
```

#### Backup de Logs:
```bash
# Linux
tar -czvf /backups/logs_$(date +%Y%m%d).tar.gz /D/Github/index/logs

# Windows
powershell Compress-Archive -Path "D:\Github\index\logs\*" -DestinationPath "D:\backups\logs_$(Get-Date -Format 'yyyyMMdd').zip"
```

#### Teste de Desempenho:
```bash
# Teste de carga com Apache Bench
ab -n 1000 -c 50 http://localhost:5000/

# Teste de resposta
curl -I --location http://localhost:5000/

# Teste de API
curl -X POST http://localhost:5000/database/generate-structure
```

#### Monitoramento:
```bash
# Acompanhar logs em tempo real (Linux/Mac)
tail -f logs/$(date +%Y-%m-%d)/site_access.log

# Acompanhar logs em tempo real (Windows PowerShell)
Get-Content logs\$(Get-Date -Format 'yyyy-MM-dd')\site_access.log -Wait

# Verificar conexões ativas
netstat -an | findstr :5000

# Verificar processos Python
tasklist | findstr python
```

### 7.3 Comandos Git

```bash
# Status do repositório
git status

# Adicionar todos os arquivos
git add -A

# Commit com mensagem
git commit -m "Descrição da alteração"

# Push para origin/main
git push origin main

# Pull de atualizações
git pull origin main

# Ver histórico de commits
git log --oneline -20

# Ver diff de arquivos modificados
git diff
git diff --cached

# Reset de arquivos (cuidado!)
git checkout -- .
git reset --hard HEAD
```

### 7.4 Fluxo Completo de Deploy (Passo a Passo)

```bash
# 1. Navegar até o diretório do projeto
cd D:\Github\index

# 2. Verificar status do Git
git status

# 3. Verificar se há atualizações remotas
git pull origin main

# 4. Adicionar alterações locais
git add -A

# 5. Verificar diff
git diff --cached --stat

# 6. Commit
git commit -m "Atualização: [descrever alterações]"

# 7. Push para GitHub
git push origin main

# 8. (Opcional) Reiniciar servidor
# No Windows:
taskkill /F /IM python.exe
start python site/main.py

# No Linux:
systemctl restart flask-site-service
# ou
pkill -f "python site/main.py"
python site/main.py &
```

---

## 8. Esquema Completo do Database

### 8.1 Arquivo Central: `philistudies.json`

- **Localização**: `D:\Github\index\database\philistudies.json`
- **Tamanho**: ~3.2MB
- **Formato**: JSON (RFC 8259)
- **Codificação**: UTF-8 (com `ensure_ascii=False`)
- **Função**: Índice completo de TODOS os arquivos do projeto

### 8.2 Estrutura do JSON

O `philistudies.json` é um objeto JSON onde cada chave representa um diretório. A estrutura segue este padrão:

```json
{
  "database_root": {
    "files": [
      {
        "id": "database/arquivo.txt",
        "name": "arquivo.txt",
        "path": "database/arquivo.txt",
        "size": 1024,
        "extension": "txt",
        "type": "file",
        "modified": 1652524800000,
        "preview": null
      }
    ],
    "folders": [
      {
        "id": "database/files",
        "name": "files",
        "path": "database/files",
        "modified": 1652524800000
      }
    ]
  },
  "database/files": {
    "files": [...],
    "folders": [...]
  },
  "database/files/dev": {
    "files": [...],
    "folders": [...]
  },
  "database/files/skills": {
    "files": [...],
    "folders": [...]
  }
}
```

### 8.3 Esquema de Categorias de Arquivos

| Tipo | Extensões | Ícone Sugerido |
|------|-----------|----------------|
| `image` | jpg, jpeg, png, gif, svg, webp | 🖼️ |
| `pdf` | pdf | 📄 |
| `archive` | zip, rar, 7z, tar, gz | 📦 |
| `code` | js, html, css, py, php, json, ts | 💻 |
| `video` | mp4, webm, ogg, mov | 🎬 |
| `audio` | mp3, wav, flac | 🎵 |
| `font` | ttf, otf, woff, woff2 | 🔤 |
| `file` | (qualquer outro) | 📎 |

### 8.4 Campos de Cada Arquivo no JSON

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `id` | string | Identificador único (caminho relativo) | `"database/files/dev/avatar/user1.png"` |
| `name` | string | Nome do arquivo | `"user1.png"` |
| `path` | string | Caminho relativo completo | `"database/files/dev/avatar/user1.png"` |
| `size` | number | Tamanho em bytes | `204800` |
| `extension` | string | Extensão sem ponto | `"png"` |
| `type` | string | Categoria do arquivo | `"image"` |
| `modified` | number | Timestamp de modificação (ms) | `1652524800000` |
| `preview` | string/null | URL de pré-visualização (apenas images) | `"database/files/dev/avatar/user1.png"` |

### 8.5 Pastas de Skills (Documentação Técnica)

Todas as 15 documentações técnicas estão em `database/files/skills/`:

| # | Arquivo | Tema |
|---|---------|------|
| 01 | `01_Database_Introducao_e_Sistemas_Gerenciadores_SGBD.md` | Introdução a Bancos de Dados e SGBDs |
| 01 | `01_Introducao_e_Conceitos.md` | Introdução e Conceitos Gerais |
| 02 | `02_Modelagem_Relacional_Entidades_Atributos_e_Relacionamentos.md` | Modelagem Relacional (ER) |
| 02 | `02_Service_Workers_e_Cache.md` | Service Workers e Cache |
| 02 | `02_Service_Workers_Fundamentos_e_Ciclo_de_Vida.md` | Fundamentos e Ciclo de Vida dos SW |
| 03 | `03_Manifest_e_Instalacao.md` | Web App Manifest e Instalação |
| 03 | `03_Manifest_Web_App_Configuracao_e_Propriedades.md` | Configuração do Manifest |
| 03 | `03_Normalizacao_de_Dados_1NF_2NF_3NF_e_BCNF.md` | Normalização de Dados |
| 04 | `04_Algebra_Relacional_e_Fundamentos_Teoricos_do_SQL.md` | Álgebra Relacional e SQL |
| 04 | `04_Capacidades_Nativas_e_TWA.md` | Capacidades Nativas e TWA |
| 04 | `04_Estrategias_de_Cache_com_Service_Workers.md` | Estratégias de Cache com SW |
| 05 | `05_Offline_Fallback_e_Experiencia_do_Usuario.md` | Fallback Offline e UX |
| 05 | `05_Otimizacao_e_Performance.md` | Otimização e Performance |
| 05 | `05_Tipos_de_Dados_SQL_e_Restricoes_Constraints.md` | Tipos de Dados SQL e Constraints |

---

## 9. Esquema Flask Python

### 9.1 Arquivo: `site/main.py` (Linha a Linha)

```python
# IMPORTS
from flask import Flask, send_file, request, jsonify
import sys
import datetime
import os
import time
import subprocess
from collections import defaultdict

# IMPORT DO ROUTER
from routes import register_routes

# CRIAÇÃO DA APP
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# RATE LIMITING
RATE_LIMIT_COUNT = 30
RATE_LIMIT_PERIOD = 10
request_counts = defaultdict(lambda: {'count': 0, 'timestamp': 0})

# CONTADORES DE VISITAS
visitas_total = 0
visitas_hoje = 0
data_atual = datetime.date.today()

# CAMINHOS
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_BASE_DIR = os.path.join(BASE_DIR, 'logs')
MAINTENANCE_DIR = os.path.join(BASE_DIR, 'maintenance')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
UPLOAD_FOLDER = os.path.join(DATABASE_DIR, 'files')

# CRIAÇÃO DE DIRETÓRIOS
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

### 9.2 Funções do Servidor

#### `get_log_file(log_type='site')`
```python
def get_log_file(log_type='site'):
    hoje_str = datetime.date.today().strftime('%Y-%m-%d')
    dia_dir = os.path.join(LOG_BASE_DIR, hoje_str)
    os.makedirs(dia_dir, exist_ok=True)
    if log_type == 'database':
        return os.path.join(dia_dir, 'database_access.log')
    return os.path.join(dia_dir, 'site_access.log')
```
- **Entrada**: Tipo de log (`'site'` ou `'database'`)
- **Saída**: Caminho completo do arquivo de log do dia
- **Comportamento**: Cria subdiretório da data automaticamente

#### `registrar_log(mensagem, log_type='site')`
```python
def registrar_log(mensagem, log_type='site'):
    try:
        with open(get_log_file(log_type), 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}")
```
- Grava mensagens com timestamp no formato `[HH:MM:SS]`
- Encoding UTF-8 para suportar emojis e acentos
- Append mode (`'a'`) — nunca sobrescreve logs anteriores

#### `atualizar_linha()`
```python
def atualizar_linha():
    log_msg = f"📊 Visitas Total: {visitas_total} | Hoje: {visitas_hoje}"
    sys.stdout.write(f"\r{log_msg}")
    sys.stdout.flush()
    registrar_log(log_msg)
```
- Exibe contador de visitas no terminal em tempo real
- Sobrescreve a linha atual do console (`\r`)

#### `generate_structure_json(specific_file=None)`
```python
def generate_structure_json(specific_file=None):
    try:
        script_path = os.path.join(DATABASE_DIR, 'generate_assets_structure.py')
        cmd = [sys.executable, script_path]
        if specific_file:
            cmd.append(specific_file)
        subprocess.run(cmd, check=True)
        msg = f"✅ Estrutura JSON {'atualizada' if specific_file else 'gerada'} com sucesso."
        registrar_log(msg, log_type='database')
        return True
    except Exception as e:
        registrar_log(f"❌ Erro ao atualizar estrutura JSON: {e}", log_type='database')
        return False
```
- Executa subprocesso Python para gerar/atualizar `philistudies.json`
- Logging de sucesso (✅) ou falha (❌)

#### `send_error_file(path, code)`
```python
def send_error_file(path, code):
    try:
        return send_file(path), code
    except:
        return f"Erro {code}", code
```

### 9.3 Middleware `before_request`

```python
@app.before_request
def security_and_tracking():
    # ... (ver Seção 14 para detalhes completos)
```

**Fluxo para CADA requisição**:
1. Ignora favicon.ico e favicon.png → retorna 204
2. Ignora extensões estáticas → passa sem logging
3. Ignora pastas estáticas → passa sem logging
4. Verifica rate limiting → bloqueia com 429 se necessário
5. Atualiza contadores de visita
6. Registra log de acesso (diferente para paths `/database`)

### 9.4 Inicialização

```python
if __name__ == '__main__':
    print("\n🚀 Servidor ONLINE na porta 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
```
- **Obrigatoriamente porta 5000** — qualquer outra porta causará falha no Cloudflare Tunnel
- **`debug=False`** — modo de produção (sem debugger exposto)
- **`host="0.0.0.0"`** — escuta em todas as interfaces (necessário para tunnel)

---

## 10. Porta 5000

### 10.1 Por que a porta 5000 é obrigatória?

A porta **5000** é configurada em **quatro locais** simultaneamente:

| Local | Configuração | Consequência de Alteração |
|-------|-------------|--------------------------|
| `site/main.py:135` | `app.run(port=5000)` | Servidor não inicia corretamente |
| `maintenance/main.py:95` | `app.run(port=5000)` | Modo manutenção conflita |
| `.cloudflared/config.yml:7` | `service: http://localhost:5000` | Tunnel não encontra backend |
| Verbos de deploy | `python site/main.py` | Nenhuma falha (usa padrão) |

### 10.2 Justificativa Técnica

1. **Cloudflare Tunnel**: O `config.yml` roteia `kendricknicoleti.com` para `localhost:5000`. Alterar exigiria atualizar o tunnel.
2. **Convenção Flask**: Porta 5000 é a porta padrão do Flask em produção.
3. **Compatibilidade**: Portas abaixo de 1024 exigem privilégios root/admin em produção.
4. **Disponibilidade**: Porta 5000 raramente é usada por outros serviços.

### 10.3 Configuração de Porta Alternativa (NÃO RECOMENDADO)

Caso absolutamente necessário, alterar em 4 arquivos:
1. `site/main.py`: `app.run(host="0.0.0.0", port=NOVA_PORTA, debug=False)`
2. `maintenance/main.py`: `app.run(host="0.0.0.0", port=NOVA_PORTA, debug=False)`
3. `.cloudflared/config.yml`: `service: http://localhost:NOVA_PORTA`
4. Reiniciar Cloudflare Tunnel: `cloudflared tunnel run`

---

## 11. Esquema Completo das Rotas

### 11.1 Mapa Completo de Rotas

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAPA DE ROTAS FLASK                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   ROTAS PÚBLICAS                         │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  GET  /                     → index.html                 │   │
│  │  GET  /calendar             → pages/calendar.html        │   │
│  │  GET  /login                → pages/login.html           │   │
│  │  GET  /go-calendar          → redirect → /calendar       │   │
│  │  GET  /go-database          → redirect → /database       │   │
│  │  GET  /go-site              → redirect → /                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  ROTAS DE DATABASE                      │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  GET  /database              → database/index.html       │   │
│  │  POST /database/upload       → upload_file()             │   │
│  │  POST /database/generate-structure → generate_structure()│   │
│  │  GET  /database/<path>       → serve_database_files()    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           ROTAS DE MANUTENÇÃO / ESTÁTICOS               │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  GET  /maintenance/<path>    → maintenance files         │   │
│  │  GET  /assets/*              → static assets             │   │
│  │  GET  /css/*                 → static CSS                │   │
│  │  GET  /js/*                  → static JavaScript          │   │
│  │  GET  /img/*                 → static imagens             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                ROTAS DE API                             │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  GET    /api/<path>          → JSON success response     │   │
│  │  POST   /api/<path>          → JSON success response     │   │
│  │  PUT    /api/<path>          → JSON success response     │   │
│  │  DELETE /api/<path>          → JSON success response     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                TRATAMENTO DE ERROS                      │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  404  → maintenance/404.html                            │   │
│  │  500  → maintenance/500.html                            │   │
│  │  429  → maintenance/429.html (rate limit)               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 11.2 Detalhamento de Cada Rota

#### `GET /`
- **Função**: Página inicial do site
- **Template**: `site/index.html`
- **Cache**: Nenhum especial
- **Acesso**: Público
- **Logs**: Registrado como acesso normal

#### `GET /calendar`
- **Função**: Calendário de orações dos últimos 12 meses
- **Template**: `site/pages/calendar.html`
- **Funcionalidades**:
  - Visualização de progresso mensal (Laudes, Hora Média, Vésperas, Completas)
  - Resumo com contagem de completas, parciais e vazias
  - Sincronização Firebase (Login/Logout)
  - Exportação e Importação de dados JSON
- **Dependências**: `calendar.js`, `suite.js`, `liturgy.js`, `firebase-sync.js`
- **Acesso**: Público (mas funcionalidade completa requer login)

#### `GET /login`
- **Função**: Página de autenticação
- **Template**: `site/pages/login.html`
- **Métodos de autenticação**:
  - Email + Senha (formulário)
  - Google Sign-In (Firebase OAuth)
- **Após login**: Redireciona para `/calendar`
- **Segurança**: reCAPTCHA pode estar implícito via Firebase

#### `POST /database/upload`
- **Função**: Upload de arquivos para o database
- **Parâmetros**:
  - `files[]` (obrigatório): Lista de arquivos no formato multipart/form-data
  - `current_path` (opcional): Caminho de destino dentro do database
- **Retorno**:
  ```json
  {
    "message": "X arquivo(s) enviados com sucesso",
    "count": X,
    "destination": "/caminho/completo"
  }
  ```
- **Códigos de erro**:
  - `400`: Nenhum arquivo enviado
  - `429`: Rate limit excedido
- **Segurança**:
  - Proteção contra path traversal
  - Sanitização de nome de arquivo (secure_filename)
  - Limite de 500MB por upload

#### `POST /database/generate-structure`
- **Função**: Forçar regeneração do `philistudies.json`
- **Retorno**: `{"status": "success"}` ou `{"status": "error"}`
- **Código de erro**: `500` se falhar

#### `GET /database/<path>`
- **Função**: Servir arquivos do database para download
- **Lógica**: Procura primeiro em `site/database/`, depois em `DATABASE_DIR`
- **Uso**: Download de documentos, templates, etc.

#### `GET /go-calendar`, `GET /go-database`, `GET /go-site`
- **Função**: Redirecionamentos amigáveis
- **Mecanismo**: `redirect(url_for(...))` do Flask
- **Código HTTP**: 302 (Found)

#### `GET/POST/PUT/DELETE /api/<path>`
- **Função**: API genérica de manutenção
- **Retorno**:
  ```json
  {
    "status": "success",
    "message": "API está funcionando normalmente durante a manutenção",
    "path": "/caminho/solicitado"
  }
  ```
- **Uso**: Verificação de saúde da API durante modo manutenção


---

## 12. Páginas de Erro

### 12.1 Páginas de Erro Personalizadas

O projeto possui **10 páginas de erro customizadas** localizadas em `maintenance/`:

| Código | Nome do Arquivo | HttpStatus | Descrição |
|--------|-----------------|------------|-----------|
| 400 | `400.html` | Bad Request | Solicitação malformada |
| 401 | `401.html` | Unauthorized | Autenticação necessária |
| 403 | `403.html` | Forbidden | Acesso proibido |
| 404 | `404.html` | Not Found | Página não encontrada |
| 405 | `405.html` | Method Not Allowed | Método HTTP não suportado |
| 429 | `429.html` | Too Many Requests | Rate limit excedido |
| 500 | `500.html` | Internal Server Error | Erro interno do servidor |
| 502 | `502.html` | Bad Gateway | Gateway inválido |
| 503 | `503.html` | Service Unavailable | Serviço indisponível (manutenção) |
| 504 | `504.html` | Gateway Timeout | Timeout do gateway |

### 12.2 Estilos das Páginas de Erro

Arquivo: `maintenance/error-pages.css`

**Características**:
- Design **dark mode** nativo
- Efeito **3D** com `box-shadow` e `transform`
- Animação de **flutuação** no título (`:float`)
- **Glassmorphism**: Fundo semi-transparente com `backdrop-filter: blur(12px)`
- **Responsivo**: Media queries para telas menores que 600px
- **Botão animado**: Hover com escala e rotação

**Classe principal**: `.error-container`
```css
.error-container {
    text-align: center;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    border: 1px solid rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    max-width: 500px;
    margin: 0 auto;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    animation: float 3s ease-in-out infinite;
}
```

### 12.3 Fluxo de Erros

```
Requisição → Flask → Rota existe?
                        ├── SIM → Processa normalmente
                        └── NÃO → errorhandler(404)
                                    ├── Carrega maintenance/404.html
                                    ├── Aplica error-pages.css
                                    └── Retorna HTTP 404

Erro interno → errorhandler(Exception)
                ├── Registra log: "❌ 500: {erro}"
                ├── Carrega maintenance/500.html
                └── Retorna HTTP 500
```

---

## 13. Sistema de Logs

### 13.1 Arquitetura de Logs

```
┌─────────────────────────────────────────────────────────┐
│                    SISTEMA DE LOGS                       │
│                                                          │
│  RAIZ: D:\Github\index\logs\                            │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ORGANIZAÇÃO POR DATA                            │    │
│  │                                                  │    │
│  │  logs/                                           │    │
│  │  ├── 2026-05-08/                                 │    │
│  │  │   ├── site.log                  (logs site)   │    │
│  │  │   ├── site_access.log          (acessos)     │    │
│  │  │   ├── database.log            (database)     │    │
│  │  │   ├── database_access.log     (acessos DB)   │    │
│  │  │   └── maintenance.log         (manutenção)   │    │
│  │  ├── 2026-05-09/                                 │    │
│  │  ├── 2026-05-11/                                 │    │
│  │  ├── 2026-05-12/                                 │    │
│  │  ├── 2026-05-13/                                 │    │
│  │  └── 2026-05-14/  ← DIA ATUAL                   │    │
│  │       ├── site.log                               │    │
│  │       ├── site_access.log                       │    │
│  │       ├── database.log                          │    │
│  │       ├── database_access.log                   │    │
│  │       └── maintenance.log                       │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  FORMATO DE CADA LINHA:                                 │
│  [HH:MM:SS] mensagem                                    │
│                                                          │
│  EXEMPLOS:                                               │
│  [14:30:25] 👤 Acesso: 192.168.1.5 -> /calendar        │
│  [14:30:25] 📊 Visitas Total: 150203 | Hoje: 3482      │
│  [14:30:26] 👤 Acesso Database: 203.0.113.45 -> /...   │
│  [14:30:30] ❌ 500: TypeError: Cannot read...           │
│  [14:30:31] ⚠️ Tentativa de path traversal bloqueada   │
│  [14:30:32] ⬆️ Upload: 192.168.1.5 enviou arquivo.pdf  │
│  [14:30:33] 🚧 Acesso em Manutenção: 10.0.0.1         │
│  [14:30:34] ⚠️ BLOQUEIO (Manutenção): IP 10.0.0.1    │
└─────────────────────────────────────────────────────────┘
```

### 13.2 Tipos de Logs

| Log | Localização | Gerado Por | Conteúdo |
|-----|------------|------------|----------|
| `site_access.log` | `logs/{data}/` | `site/main.py` | Todos os acessos ao site |
| `database_access.log` | `logs/{data}/` | `site/main.py` | Acessos a `/database/*` |
| `site.log` | `logs/{data}/` | `site/main.py` | Logs gerais do site |
| `database.log` | `logs/{data}/` | `site/main.py` | Logs de upload e estrutura |
| `maintenance.log` | `logs/{data}/` | `maintenance/main.py` | Logs do modo manutenção |

### 13.3 Funcionalidade de Log no Código

```python
# No site/main.py:
def registrar_log(mensagem, log_type='site'):
    try:
        with open(get_log_file(log_type), 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}")
```

### 13.4 Estrutura de Diretórios de Logs

```
logs/
├── 2026-05-08/
│   ├── site.log
│   ├── site_access.log
│   ├── database.log
│   ├── database_access.log
│   └── maintenance.log
├── 2026-05-09/
├── 2026-05-11/
├── 2026-05-12/
├── 2026-05-13/
└── 2026-05-14/  (DIA ATUAL)
```

---

## 14. Proteções Contra Ameaças

### 14.1 Camadas de Segurança

```
┌──────────────────────────────────────────────────────────┐
│              CAMADAS DE SEGURANÇA                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  CAMADA 1: CLOUDFLARE WAF                        │    │
│  │  ├── Proteção DDoS L3/L4/L7                     │    │
│  │  ├── Regras OWASP Top 10                         │    │
│  │  ├── Rate limiting automático                    │    │
│  │  ├── IP reputation scoring                      │    │
│  │  └── Bot detection                              │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────┐    │
│  │  CAMADA 2: CLOUDFLARE CDN                       │    │
│  │  ├── Cache Edge (TTL configurável)             │    │
│  │  ├── Always Online (cache em falha)            │    │
│  │  ├── Auto Minify (HTML/CSS/JS)                │    │
│  │  ├── Brotli Compression                        │    │
│  │  └── SSL/TLS (Full Strict)                    │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────┐    │
│  │  CAMADA 3: FIREWALL DE APLICAÇÃO (Flask)       │    │
│  │  ├── Rate Limiting (30 req/10s por IP)          │    │
│  │  ├── Input sanitization (secure_filename)       │    │
│  │  ├── Path traversal protection                  │    │
│  │  ├── Upload size limit (500MB)                  │    │
│  │  ├── Error handling (sem stack traces)          │    │
│  │  └── Ignora requests estáticos                  │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────┐    │
│  │  CAMADA 4: AUTENTICAÇÃO                         │    │
│  │  ├── Firebase Authentication                    │    │
│  │  ├── Google OAuth 2.0                           │    │
│  │  ├── Token JWT (se implementado)                 │    │
│  │  └── Cookie sameSite=Strict                     │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────┐    │
│  │  CAMADA 5: MONITORAMENTO                        │    │
│  │  ├── Logs de acesso em tempo real                │    │
│  │  ├── Detecção de path traversal                  │    │
│  │  ├── Rate limit logging                          │    │
│  │  └── Dashboard de visitas                        │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### 14.2 Rate Limiting — Implementação Detalhada

#### No Servidor Principal (`site/main.py`):
```python
RATE_LIMIT_COUNT = 30  # Máximo de requisições
RATE_LIMIT_PERIOD = 10  # Período em segundos
request_counts = defaultdict(lambda: {'count': 0, 'timestamp': 0})

# Na before_request:
client_ip = request.remote_addr
current_time = time.time()

if current_time - request_counts[client_ip]['timestamp'] > RATE_LIMIT_PERIOD:
    request_counts[client_ip] = {'count': 1, 'timestamp': current_time}
else:
    request_counts[client_ip]['count'] += 1

if request_counts[client_ip]['count'] > RATE_LIMIT_COUNT:
    return send_error_file(os.path.join(MAINTENANCE_DIR, '429.html'), 429)
```

#### No Modo Manutenção (`maintenance/main.py`):
```python
RATE_LIMIT_COUNT = 10  # Mais restritivo!
RATE_LIMIT_PERIOD = 10
# Mesma lógica, mas com limite 3x menor
```

**Comportamento**:
- Cada IP tem um contador resetado a cada 10 segundos
- Se exceder o limite, recebe página 429.html
- Log automático de bloqueios

### 14.3 Proteção contra Path Traversal

```python
# No upload_file():
real_database = os.path.realpath(os.path.normpath(DATABASE_DIR))
real_proposed = os.path.realpath(proposed_dest)

if real_proposed.startswith(real_database):
    dest_folder = real_proposed
else:
    registrar_log(f"⚠️ Tentativa de path traversal bloqueada: {current_path_param}", log_type='database')
    dest_folder = UPLOAD_FOLDER
```

**Como funciona**:
1. Pega o caminho absoluto real do database
2. Resolve o caminho proposto (elimina `../` e symlinks)
3. Verifica se o caminho proposto começa com o caminho do database
4. Se NÃO começar → BLOQUEIA e registra log

### 14.4 Sanitização de Nomes de Arquivo

```python
filename = secure_filename(file.filename)
```
- Importado de `werkzeug.utils`
- Remove caracteres especiais, espaços, e path separators
- Exemplo: `../../etc/passwd` → `etc_passwd`

### 14.5 Limite de Tamanho de Upload

```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
```
- Qualquer upload maior que 500MB é automaticamente rejeitado pelo Flask
- Retorna HTTP 413 (Request Entity Too Large)

### 14.6 Ignorância de Arquivos Estáticos no Logging

```python
extensoes_ignoradas = (
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', 
    '.woff', '.woff2', '.ttf', '.otf', '.json', '.map', '.ico'
)
pastas_ignoradas = ('/assets/', '/css/', '/js/', '/img/', '/src/', '/maintenance/')
```
- Reduz poluição de logs
- Melhora performance (sem logging desnecessário)
- Favicon retorna 204 (No Content)

### 14.7 Proteção DDoS Cloudflare

Ativada automaticamente pelo plano Cloudflare:
- **Always On**: Proteção 24/7 contra L3/L4/L7
- **JS Challenge**: Desafia bots antes de liberar acesso
- **CAPTCHA**: Para tráfego suspeito
- **Under Attack Mode**: Pode ser ativado via painel Cloudflare

---

## 15. Comando de Atualização Completa

### 15.1 Script de Atualização Completa (Linux/Mac)

```bash
#!/bin/bash
# ============================================
# ATUALIZAÇÃO COMPLETA DO PROJETO
# D:\Github\index — Atualizar e commitar tudo
# ============================================

set -e  # Sair se qualquer comando falhar

# Navegar até o diretório do projeto
cd /mnt/d/Github/index || cd D:/Github/index || (echo "ERRO: Diretório não encontrado"; exit 1)

echo "============================================"
echo " ATUALIZAÇÃO COMPLETA DO PROJETO"
echo "============================================"
echo ""

# 1. Verificar status atual
echo "[1/6] Verificando status do Git..."
git status --short

# 2. Adicionar TODAS as alterações
echo "[2/6] Adicionando todos os arquivos ao staging..."
git add -A

# 3. Verificar diff resumido
echo "[3/6] Verificando alterações..."
git diff --cached --stat || echo "Nenhuma alteração para commitar."

# 4. Commit (somente se houver mudanças)
echo "[4/6] Criando commit..."
if ! git diff --cached --quiet; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Atualização automática - $TIMESTAMP"
    echo "✅ Commit criado com sucesso!"
else
    echo "⏭ Nenhuma mudança para commitar."
fi

# 5. Push para GitHub
echo "[5/6] Enviando para GitHub..."
git push origin main 2>/dev/null || git push origin HEAD

# 6. Regenerar estrutura JSON do database
echo "[6/6] Regenerando estrutura do database..."
python3 database/generate_assets_structure.py || echo "⚠️ Aviso: falha ao regenerar estrutura JSON"

echo ""
echo "============================================"
echo " ✅ ATUALIZAÇÃO COMPLETA FINALIZADA!"
echo " Data: $TIMESTAMP"
echo "============================================"
```

### 15.2 Script de Atualização (Windows — Batch)

```batch
@echo off
REM ============================================
REM ATUALIZAÇÃO COMPLETA DO PROJETO
REM D:\Github\index
REM ============================================

cd /d %~dp0

echo ============================================
echo  ATUALIZAÇÃO COMPLETA DO PROJETO
echo ============================================
echo.

REM 1. Adicionar todos os arquivos
echo [1/4] Adicionando todos os arquivos...
git add -A

REM 2. Verificar se há mudanças
echo [2/4] Verificando alteracoes...
git diff --cached --quiet
IF %ERRORLEVEL%==0 (
    echo Nenhuma alteracao detectada.
    goto :end
)

REM 3. Commit
echo [3/4] Criando commit...
for /f "tokens=1-4 delims=:. " %%a in ("%time%") do (
    set TIMESTAMP=%date% %%a:%%b:%%c
)
git commit -m "Atualizacao automatica - %TIMESTAMP%"

REM 4. Push
echo [4/4] Enviando para GitHub...
git push origin main

REM 5. Regenerar estrutura
echo Regenerando estrutura JSON...
python database\generate_assets_structure.py

echo.
echo ============================================
echo  ATUALIZACAO COMPLETA FINALIZADA!
echo ============================================
pause

:end
echo ============================================
echo  FIM - Nenhuma alteracao para commitar.
echo ============================================
pause
```

### 15.3 Comando de Atualização Rápida (Uma Linha)

```bash
# Linux/Mac (Git Bash no Windows)
cd D:/Github/index && git add -A && git commit -m "Auto update" && git push && python3 database/generate_assets_structure.py

# Windows CMD
cd D:\Github\index && git add -A && git commit -m "Auto update" && git push && python database\generate_assets_structure.py

# Windows PowerShell
cd D:\Github\index; git add -A; git commit -m "Auto update"; git push; python database\generate_assets_structure.py
```

### 15.4 Git Hooks (Automatização)

O projeto inclui hooks no `.git/hooks/`:

| Hook | Arquivo | Função |
|------|---------|--------|
| `pre-commit` | `pre-commit.sample` | Executado antes do commit |
| `post-update` | `post-update.sample` | Executado após push (trigger para deploy) |
| `pre-push` | `pre-push.sample` | Executado antes do push |
| `commit-msg` | `commit-msg.sample` | Valida mensagem de commit |
| `prepare-commit-msg` | `prepare-commit-msg.sample` | Prepara mensagem de commit |

**Para ativar um hook**, renomeie o arquivo de `.sample` para sem extensão:
```bash
mv .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 15.5 GitHub Actions (CI/CD Sugerido)

Criar arquivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy Project

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install flask sqlalchemy pandas werkzeug
    
    - name: Generate assets structure
      run: python database/generate_assets_structure.py
    
    - name: Deploy to server
      run: |
        # Adicione aqui seus comandos de deploy
        echo "Deploying to production server..."
        # ssh user@server 'cd /path && git pull && systemctl restart flask-app'
    
    - name: Notification
      run: echo "✅ Deploy completed successfully!"
```

---

## 16. Glossário Técnico

| Termo | Definição |
|-------|-----------|
| **Flask** | Micro-framework web em Python |
| **Werkzeug** | Biblioteca WSGI que o Flask usa internamente |
| **SQLAlchemy** | ORM (Object-Relational Mapping) para Python |
| **Pandas** | Biblioteca de análise/manipulação de dados |
| **Firebase** | Plataforma BaaS (Backend as a Service) do Google |
| **CDN** | Content Delivery Network — rede de distribuição de conteúdo |
| **WAF** | Web Application Firewall — firewall de aplicação web |
| **DDoS** | Distributed Denial of Service — ataque de negação de serviço distribuída |
| **Tunnel** | Túnel reverso para expor servidor local à internet |
| **JWT** | JSON Web Token — padrão para tokens de autenticação |
| **ORM** | Object-Relational Mapping — mapeamento objeto-relacional |
| **PWA** | Progressive Web App — aplicação web progressiva |
| **REST** | Representational State Transfer — arquitetura de APIs |
| **OAuth** | Protocolo de autorização padrão |
| **Rate Limiting** | Limitação de taxa de requisições |
| **Path Traversal** | Ataque explorando navegação de diretórios |
| **CSRF** | Cross-Site Request Forgery — falsificação de requisição entre sites |
| **XSRF** | Variante de CSRF |
| **CORS** | Cross-Origin Resource Sharing — compartilhamento de recursos entre origens |
| **SSL/TLS** | Protocolos de criptografia de comunicação |
| **Brotli** | Algoritmo de compressão de dados |
| **Minify** | Remoção de espaços/comments de código para reduzir tamanho |
| **TTL** | Time To Live — tempo de vida do cache |
| **Edge** | Nó de borda da CDN, mais próximo do usuário final |
| **Service Worker** | Script que roda em background, habilitando funcionalidades offline |
| **Web Worker** | Script que roda em thread separada no navegador |

---

## 17. Informações Adicionais

### 17.1 Ambientes

| Ambiente | URL | Descrição |
|----------|-----|-----------|
| **Produção** | `kendricknicoleti.com` | Site público via Cloudflare Tunnel |
| **Desenvolvimento Local** | `localhost:5000` | Servidor Flask direto na máquina |
| **Manutenção** | `localhost:5000` | Modo manutenção (substitui app principal) |

### 17.2 Estrutura de Branches Git

| Branch | Status | Descrição |
|--------|--------|-----------|
| `main` | Ativo ✅ | Branch principal de produção |
| — | — | Não há branches secundários documentados |

### 17.3 Commits Recentes

```
fff2dac Auto update
6ff8382 Auto update
22ea6ae Auto update
a702987 Auto update
2075c63 Auto update
```

Todos os commits usam a mensagem "Auto update", gerados automaticamente pelo `up_git.bat`.

### 17.4 Recursos Especiais

| Recurso | Status | Descrição |
|---------|--------|-----------|
| Cloudflare Tunnel | ✅ Ativo | Proxy reverso para servidor local |
| DDoS Protection | ✅ Ativo | Proteção automática Cloudflare |
| CDN Cache | ✅ Ativo | Distribuição global de conteúdo estático |
| Service Workers | ✅ Documentado | Cache offline PWA |
| Firebase Auth | ✅ Integrado | Login Google |
| Rate Limiting | ✅ Ativo | 30 req/10s app, 10 req/10s manutenção |
| Path Traversal Protection | ✅ Ativo | Validação em upload |
| File Size Limit | ✅ 500MB | Máximo por upload |
| Auto-update Script | ✅ Funcional | up_git.bat para Windows |
| Daily Log Rotation | ✅ Ativo | Novo diretório por dia |
| JSON Asset Index | ✅ 3.2MB | philistudies.json com ~2500+ entradas |
| Error Pages | ✅ 10 páginas | 400, 401, 403, 404, 405, 429, 500, 502, 503, 504 |
| Dark Mode | ✅ Nativo | Tema escuro padrão |
| PWA (Progressive Web App) | ✅ Configurado | Manifest, Service Workers, ícones |
| Responsive Design | ✅ Mobile CSS | CSS adaptado para dispositivos móveis |

---

## 18. Nota Final

Este README foi gerado a partir da **análise completa** de todos os arquivos do projeto `D:\Github\index`. Cada seção reflete o comportamento real do código, sem informações inventadas.

> ⚠️ **IMPORTANTE**: A porta **5000** é **fixa e obrigatória**. Qualquer alteração requer atualização em pelo menos 3 locais e reinicialização do Cloudflare Tunnel.

> 📌 Para manter este documento atualizado, execute o comando de atualização completa após cada modificação no projeto.

---

*Documentação gerada em: 2026-05-14*
*Último commit: Auto update*
*Autor do projeto: kendrick3004*

---

## 19. Histórico de Modificações

### [2026-05-22 20:30]
- **Expansão do Calendário (365 Dias)**: Removida a trava de data que impedia a visualização de progresso futuro. O calendário agora processa e exibe estatísticas para o ano completo (365 dias) de forma fluida.
- **Sincronização de Autenticação (Cookies)**: Implementada a geração automática do cookie `firebase_auth_token` no frontend após o login com Google/Firebase. Isso resolve o problema de redirecionamento indevido em rotas protegidas do backend (upload/download).
- **Estrutura de Temporários (.temp)**: Reorganizada a pasta `.temp` com subpastas `.repo` (para clones) e `.zip` (para histórico persistente de downloads). Adicionados arquivos `.gitkeep` para preservar a estrutura no Git.
- **Correção de Inicialização (Boot)**: Resolvido um erro crítico de `ImportError` em `site/routes.py` causado por uma referência de função desatualizada após a migração para o módulo `.system`.
- **Arquitetura do Sistema (.system)**: Criada a pasta oculta `.system` para centralizar utilitários e lógica interna do servidor.
- **Centralização de Zipagem**: Movida a lógica de compressão de arquivos para `.system/utils/zip_manager.py`, permitindo que múltiplos módulos (site, database, temas) utilizem o mesmo sistema de compartilhamento de forma modular.
- **Organização Estrutural**: A pasta `maintenance` foi mantida na raiz por requisito operacional, mas os scripts de inicialização e rotas foram validados para garantir a coexistência com a nova estrutura `.system`.
- **Centralização de Credenciais (.env)**: Criado arquivo `.env` na raiz do projeto para armazenar de forma segura o token do Cloudflare, chaves de API do Firebase e do WeatherAPI.
- **Segurança e Configuração**: Refatorado `setup.sh` para dividir comandos complexos e carregar tokens via variáveis de ambiente. Removidas referências hardcoded de tokens em `start.sh` e `start_copy.sh`.
- **Correção de Lógica no Database**: Corrigida a geração de `json_key` em `generate_assets_structure.py` para evitar conflitos no diretório raiz e garantir compatibilidade de caminhos (Linux style).
- **Otimização de Performance (Upload)**: Modificada a rota de upload em `site/routes.py` para realizar uma única atualização da estrutura JSON após o envio de múltiplos arquivos, eliminando processamento redundante.
- **Melhoria no Rate Limiting e Segurança**: Ajustada a lógica de bloqueio em `site/main.py` para usar `startswith` em pastas ignoradas, evitando falsos positivos. Reforçada a proteção contra Path Traversal em `site/routes.py` com verificação rigorosa de separadores de diretório.
- **Modo Manutenção**: Corrigida a lógica de servimento de Favicon em `maintenance/main.py` e adicionado tratamento de erros robusto no sistema de logging.
- **Qualidade de Código**: Adicionadas docstrings em todas as funções críticas e padronizada a nomenclatura para snake_case.
- **Checklist de Controle**: Criado o arquivo `Oque foi feito` para rastreamento contínuo de melhorias.

### [2026-05-17 15:15]
- **Otimização de Download (ZIP no Servidor)**: A rota `/database/download-zip` em `routes.py` foi otimizada para processar a compactação inteiramente no servidor usando `BytesIO`. O arquivo ZIP é gerado em memória e enviado via streaming diretamente para o navegador, eliminando a lentidão de processamento no cliente e evitando o uso de disco permanente no servidor.
- **Fundo Fixo Universal**: Implementada técnica de pseudo-elemento (`body::before`) com `position: fixed` em `modes.css`. Isso garante que a imagem de fundo permaneça estática e cubra 100% da tela em todos os dispositivos (Desktop e Mobile), eliminando espaços vazios ao rolar a página na Suite, Calendário e Login.
- **Correção de Navegação**: Removido o interceptor de login para o Calendário em `site/pages/suite/suite.js`. O calendário agora possui acesso público direto da página inicial, corrigindo o bug de redirecionamento indevido.
- **Ajuste Visual na Suite**: Refinamento dos cards da Liturgia das Horas na Suite principal. Quando uma oração é completada, o card agora exibe uma borda verde mais grossa (3px) com um detalhe em amarelo/dourado (outline), restaurando o visual clássico solicitado.
- **Documentação**: Atualização completa do `README.md` com o histórico detalhado das alterações realizadas nesta sessão.

### [2026-05-22 21:00]
- **Correção: Notificações Sobrepostas** — A função `showNotification` em `site/database/js/state.js` foi refatorada para empilhar as notificações verticalmente em vez de sobrepô-las. Cada nova notificação é posicionada abaixo da anterior usando cálculo dinâmico de `offsetHeight`. O CSS em `styles.css` recebeu `transition: top 0.2s ease` para animar o reposicionamento após remoção.
- **Correção: ZIP Vazio no Download** — Identificado e corrigido o bug crítico de path duplo: o frontend enviava `database/files/dev` para o servidor, mas o `zip_manager.py` já recebe caminhos relativos ao `DATABASE_DIR` (que é `database/`), resultando em `database/database/files/dev` (inexistente). A função `downloadZipFromServer` em `selection.js` agora remove o prefixo `database/` antes de enviar. O `zip_manager.py` também foi reforçado com remoção defensiva do prefixo e validação de `files_added > 0`.
- **Correção: Cálculo de Tamanho Duplicado** — Adicionada a função `isContainedInSelectedFolder` em `file-loader.js` que evita dupla contagem ao calcular o tamanho total da seleção. Quando uma pasta e seus arquivos filhos estão selecionados simultaneamente, apenas o tamanho da pasta é contabilizado.
- **Correção: Pasta Aparecendo Vazia no Breadcrumb** — O `updateBreadcrumb` em `file-loader.js` reconstruía o path como `database/dev` ao clicar no breadcrumb, mas a chave real no JSON é `database/files/dev`. Corrigido para usar o prefixo `database/files/` ao reconstruir os caminhos de navegação.
- **Correção: URL com Parâmetros Query** — O `pushState` em `loadFilesFromPath` agora sempre define a URL como `/database` independentemente da pasta navegada, eliminando o `?path=database/files/dev` da barra de endereços.
- **Melhoria: Download de Múltiplos Arquivos via ZIP** — Quando múltiplos arquivos são selecionados (sem pastas), o sistema agora usa compactação no servidor em vez de disparar múltiplos downloads simultâneos. Download direto só ocorre para seleção de 1 arquivo único.
- **Arquivos Modificados**: `site/database/js/state.js`, `site/database/js/file-loader.js`, `site/database/js/selection.js`, `site/database/styles.css`, `.system/utils/zip_manager.py`

### [2026-05-22 21:30]
- **Centralização de Segredos e Chaves de API** — Realizada a refatoração completa para remover chaves hardcoded dos arquivos de código fonte.
- **Novo Endpoint `/api/config`** — Criado endpoint no `main.py` que lê as chaves do Firebase e Weather do arquivo `.env` e as fornece de forma segura para o frontend.
- **Refatoração do `env-loader.js`** — O carregador de ambiente do frontend agora busca as configurações dinamicamente do servidor via `fetch('/api/config')`, eliminando a necessidade de manter chaves no código JS.
- **Firebase e Weather Dinâmicos** — Os módulos `firebase-config.js` e `weather.js` foram atualizados para aguardar o carregamento assíncrono das chaves antes da inicialização.
- **Segurança no `setup.sh`** — Removido o token do Cloudflare Tunnel que estava hardcoded. O script agora exige que o token esteja presente no `.env`, aumentando a proteção das credenciais de rede.
- **Carregamento de `.env` no `start.sh`** — Adicionada lógica para exportar variáveis do `.env` durante o processo de boot, garantindo que o ambiente esteja configurado corretamente para o Flask e serviços auxiliares.
- **Arquivos Modificados**: `site/main.py`, `site/src/js/main/env-loader.js`, `site/src/js/main/firebase-config.js`, `setup.sh`, `start.sh`.

### [2026-05-22 21:45]
- **Correção: Login com Google e Firebase Assíncrono** — Resolvido o problema onde o botão de login com Google não funcionava. Devido ao novo carregamento dinâmico de chaves do `.env`, o Firebase agora inicializa de forma assíncrona.
- **Sincronização de Inicialização** — Implementada a função `window.waitForFirebase()` no `firebase-config.js`, que permite que outros scripts aguardem a conclusão do carregamento das chaves e do SDK antes de realizar chamadas de autenticação.
- **Refatoração da Página de Login** — O `login.html` e o `login-firebase.js` foram atualizados para utilizar o novo mecanismo de espera, garantindo que `firebase.auth()` esteja disponível antes de qualquer interação do usuário.
- **Arquivos Modificados**: `site/src/js/main/firebase-config.js`, `site/pages/login.html`, `site/pages/login/login-firebase.js`.

### [2026-05-22 21:55]
- **Sincronização Final de Produção** — Todas as melhorias validadas nos arquivos de teste (`setup_copy.sh` e `start_copy.sh`) foram migradas para os arquivos oficiais (`setup.sh` e `start.sh`).
- **Compatibilidade Ubuntu 24.04** — O instalador oficial agora suporta o ambiente gerenciado externamente do Ubuntu 24.04, utilizando as flags de escape do pip.
- **Robustez do Cloudflare Tunnel** — O processo de instalação do túnel como serviço systemd foi padronizado nos scripts oficiais, garantindo persistência.
- **Ambiente Centralizado** — O carregamento de variáveis do `.env` foi padronizado para usar o comando `source`, garantindo que o token do Cloudflare e as chaves de API estejam sempre disponíveis para o sistema e para o Flask.
