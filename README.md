# Visão Geral do Projeto: Sistema Full-Stack com Gerenciador de Arquivos

Este projeto é um sistema full-stack robusto que integra um site principal com um gerenciador de arquivos (denominado "Database"). Ele foi desenvolvido para oferecer uma solução completa para gerenciamento e acesso a conteúdo, utilizando uma combinação de tecnologias modernas para backend, frontend, autenticação e infraestrutura de rede.

## Funcionalidades Principais

*   **Site Principal:** Interface web para acesso geral ao conteúdo.
*   **Gerenciador de Arquivos (Database):** Um sistema dedicado para upload, download, organização e visualização de arquivos.
*   **Autenticação de Usuários:** Integração com Firebase para login seguro via Google, com persistência de sessão de 7 dias.
*   **Segurança Robusta:** Implementação de rate limiting no frontend e proteção contra path traversal no backend para garantir a integridade e disponibilidade do sistema.
*   **Infraestrutura de Rede:** Utilização de Cloudflare Tunnels para exposição segura dos serviços, com dois túneis independentes para o site principal e o gerenciador de arquivos.
*   **Páginas de Erro Personalizadas:** Conjunto completo de 10 páginas de erro customizadas para uma experiência de usuário aprimorada em caso de falhas.
*   **Automação de Deploy:** Scripts para atualização automática do repositório e inicialização dos serviços.
*   **Geração de Estrutura de Assets:** Script para indexar arquivos e gerar um JSON de estrutura (`philistudies.json`), facilitando o gerenciamento de assets.

## Tecnologias Utilizadas

| Categoria         | Tecnologia           | Descrição                                                              |
| :---------------- | :------------------- | :--------------------------------------------------------------------- |
| **Backend**       | Flask (Python)       | Framework web para o servidor principal e lógica de API.               |
| **Frontend**      | HTML, CSS, JavaScript| Interfaces de usuário para o site e o gerenciador de arquivos.         |
| **Autenticação**  | Firebase             | Serviço de autenticação para login de usuários.                        |
| **Sincronização** | Firebase             | Sincronização de dados e estado de autenticação.                       |
| **Infraestrutura**| Cloudflare Tunnels   | Exposição segura de serviços locais para a internet.                   |
| **Gerenciamento de Assets** | Python Script (`generate_assets_structure.py`) | Geração de índice JSON de arquivos. |
| **Automação**     | Shell Script (`.sh`), Batch Script (`.bat`) | Scripts para deploy, inicialização e atualização. |

## Estrutura do Projeto

O projeto é organizado em três diretórios principais:

```
. (raiz do projeto)
├── database/             # Lógica e armazenamento do gerenciador de arquivos
│   ├── files/            # Local físico onde os arquivos são armazenados
│   ├── generate_assets_structure.py # Script para gerar philistudies.json
│   └── philistudies.json # Índice JSON dos assets
├── maintenance/          # Páginas de erro e modo de manutenção
│   ├── 400.html
│   ├── 401.html
│   ├── ... (outras páginas de erro)
│   ├── 504.html
│   ├── main.py           # Servidor Flask para páginas de manutenção
│   └── rate-limiter.js   # Lógica de rate limiting para o frontend
├── site/                 # Site principal e frontend do gerenciador de arquivos
│   ├── assets/           # Assets estáticos (imagens, CSS, JS)
│   ├── database/         # Frontend do gerenciador de arquivos
│   │   ├── app.js        # Lógica JavaScript do gerenciador de arquivos
│   │   ├── index.html    # Página principal do gerenciador de arquivos
│   │   └── js/           # Scripts JavaScript específicos do database
│   ├── pages/            # Páginas específicas do site (ex: login, calendário)
│   ├── src/              # Código fonte do frontend (JS, CSS)
│   │   ├── js/main/      # Scripts JavaScript principais
│   │   │   ├── auth-gate.js      # Lógica de autenticação
│   │   │   └── rate-limiter.js   # Lógica de rate limiting
│   │   └── styles/       # Estilos CSS
│   ├── index.html        # Página principal do site
│   ├── main.py           # Ponto de entrada do servidor Flask do site
│   └── routes.py         # Definição das rotas do servidor Flask
├── AGENTS.md             # Diretrizes para Agentes de IA
├── README.md             # Este arquivo
├── a fazer.md            # Lista de tarefas e melhorias futuras
├── RELATORIO_MELHORIAS.md # Relatório de melhorias implementadas
├── setup.sh              # Script de configuração inicial
├── setup_tunnels.sh      # Script para configurar túneis Cloudflare
├── start.sh              # Script para iniciar os serviços
└── up_git.bat            # Script de automação para atualização do Git
```

## Configuração e Instalação

1.  **Clonar o Repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd index
    ```
2.  **Configurar Cloudflare Tunnels:**
    Edite o arquivo `setup_tunnels.sh` com seus tokens de Cloudflare Tunnel e execute-o:
    ```bash
    ./setup_tunnels.sh
    ```
3.  **Instalar Dependências:**
    As dependências Python são `Flask`, `SQLAlchemy`, `Pandas` e `Werkzeug`. Embora não haja um `requirements.txt` explícito, o script de CI/CD (mencionado no `README.md` original) indica a instalação dessas bibliotecas. Certifique-se de tê-las instaladas:
    ```bash
    pip install Flask SQLAlchemy pandas Werkzeug
    ```
4.  **Inicializar o Projeto:**
    Execute o script `start.sh` para iniciar o servidor Flask e gerar a estrutura de assets:
    ```bash
    ./start.sh
    ```

## Uso

Após a inicialização, o site estará acessível através dos domínios configurados nos Cloudflare Tunnels. O gerenciador de arquivos estará disponível em uma rota específica (ex: `/database`).

## Segurança

*   **Autenticação Firebase:** Gerencia o acesso de usuários com login via Google.
*   **Rate Limiting:** Implementado no frontend (`site/src/js/main/rate-limiter.js`) para prevenir abusos, com um limite de 100 requisições a cada 5 segundos para operações de compactação.
*   **Proteção contra Path Traversal:** O backend valida os caminhos de upload para evitar acesso indevido a diretórios.

## Automação

*   **`up_git.bat`:** Um script para Windows que automatiza o processo de `git add -A`, `git commit` (com mensagem "Auto update") e `git push` para manter o repositório atualizado.
*   **`generate_assets_structure.py`:** Script Python localizado em `database/` que escaneia a pasta `database/files/` e gera ou atualiza o arquivo `philistudies.json`, que indexa todos os assets do projeto. Este script deve ser executado sempre que houver adição ou remoção manual de arquivos.

## Notas Importantes

*   **`philistudies.json`:** Este arquivo é crucial para o funcionamento do gerenciador de arquivos. Ele deve ser atualizado sempre que houver mudanças nos arquivos físicos.
*   **Responsividade Mobile:** Testes de responsividade são importantes, especialmente na faixa de 1024px-1028px.
*   **Logs:** O sistema gera logs diários para acesso ao site e ao database, armazenados em diretórios específicos.

## Melhorias Futuras (Baseado em `a fazer.md`)

O projeto possui uma lista de melhorias e desafios a serem abordados, principalmente relacionados à compactação de arquivos e performance:

*   **Compactação de Arquivos:**
    *   Suporte a múltiplos arquivos grandes.
    *   Otimização para velocidade e uso de streaming.
    *   Redução do uso de memória e prevenção de travamentos/crashes.
    *   Garantir estabilidade com arquivos pesados e compatibilidade com Cloudflare Tunnel.
    *   Manter o servidor responsivo durante a compactação.
    *   Refatorar a lógica de compactação, implementar processamento assíncrono, filas/background tasks, compressão incremental e streaming ZIP.
    *   Implementar limites inteligentes, melhorar timeout e buffer, e reorganizar upload/download.
*   **Análise de Logs e Debugging:**
    *   Identificar a causa exata de crashes, verificando carregamento de arquivos na RAM, eficiência da montagem ZIP, bloqueio do event loop, falsos erros de DoS, interpretação do Cloudflare como tráfego abusivo e timeouts entre túnel e servidor.

## Solução de Problemas

*   **Erro 500 na rota `/database`:** Verificado e corrigido um bug relacionado a `render_template` usando barras invertidas, que causava erro 500. A solução envolveu garantir que o Database não faça requisições desnecessárias a arquivos da pasta `assets` do site principal.
*   **Túnel Cloudflare:** O túnel agora roda em segundo plano, liberando o terminal. Em caso de falha no túnel, o sistema mantém o modo de manutenção para segurança.

## Atualizações Recentes (16 de Maio de 2026)

### 📱 Correção de Background Mobile
*   **Problema:** Imagens de fundo não apareciam em dispositivos móveis (iOS/Android) devido ao uso de `background-attachment: fixed`.
*   **Solução:** Implementada media query em `modes.css`, `login.css` e `calendar.html` para alternar para `background-attachment: scroll` em telas menores que 1024px, garantindo a visibilidade das imagens de fundo em todos os dispositivos.

### 🔐 Lógica de Autenticação e Redirecionamento Inteligente
*   **Verificação Antecipada:** A Suite agora verifica o estado de login assim que o usuário acessa a página inicial.
*   **Interceptação de Navegação:** Cliques nos links "Calendário" e "Database" na Suite agora são interceptados. Se o usuário não estiver logado, ele é redirecionado para a página de login com um parâmetro `redirect` preservando seu destino original.
*   **Fluxo de Login Corrigido:** O login (tanto via Email quanto Google) agora respeita o parâmetro `redirect`. Após a autenticação bem-sucedida, o usuário é levado automaticamente para a página que tentou acessar inicialmente (Calendário ou Database), em vez de ser sempre enviado para o Calendário.
*   **Melhoria no Auth Gate:** O `auth-gate.js` foi ajustado para permitir a visualização da Suite sem redirecionamento forçado, delegando a proteção para o momento da navegação ou acesso direto a rotas restritas.

---

**Autor:** Manus AI
**Data:** 16 de Maio de 2026
