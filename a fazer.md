# CHECKLIST DE TAREFAS

- [x] **MOBILE / RESPONSIVIDADE**
    - [x] Revisar telas entre 1024px e 1028px
    - [x] Ajustar responsividade das abas
    - [x] Alinhar botões (manter na mesma linha até 1024px)
    - [x] Corrigir comportamento das linhas (sem quebra para baixo)
    - [x] Revisar CSS (overflows, flex/grid, padding/margin)
- [x] **AUTENTICAÇÃO OBRIGATÓRIA**
    - [x] Implementar bloqueio de acesso sem login
    - [x] Configurar persistência de 7 dias
    - [x] Implementar limpeza de sessão após expiração
    - [x] Garantir redirecionamento automático pós-login
    - [x] Integrar lógica no Calendário (botão Conectar)
- [x] **SEPARAÇÃO DOS TÚNEIS CLOUDFLARE**
    - [x] Configurar Túnel Raiz (kendricknicoleti.com)
    - [x] Configurar Túnel Database (database.kendricknicoleti.com)
    - [x] Apontar subdomínio para `site/database/index.html`
    - [x] Criar arquivos de configuração e serviços systemd
- [x] **SISTEMAS COMPARTILHADOS**
    - [x] Padronizar redirecionamento de URLs
    - [x] Configurar páginas de erro e fallback comuns
- [x] **COMPACTAÇÃO DE ARQUIVOS / PERFORMANCE**
    - [x] Investigar lentidão e crashes na compactação
    - [x] Analisar consumo de RAM e CPU (evitar carregar tudo na memória)
    - [x] Implementar Streaming ZIP / Processamento Assíncrono (Ajustado via Rate Limiter)
    - [x] Corrigir possíveis problemas de timeout e falso DoS

---

Quero que você revise e finalize toda a estrutura do sistema Database na versão mobile e também toda a lógica de autenticação e separação dos túneis Cloudflare. Mas antes crie um checkliste de tudo que tem quefazer no começo desse arquivo e vai preenchendo para nao sep perder.

IMPORTANTE:
O código já está praticamente pronto e funcional. Os erros principais já foram corrigidos. Quero apenas revisão, ajustes finais, organização e melhorias estruturais.

──────────────────────────────
MOBILE / RESPONSIVIDADE
──────────────────────────────

Na versão mobile do Database eu já fiz várias adaptações.

Preciso que você revise principalmente:

* telas próximas de 1024px até 1028px;
* responsividade das abas;
* alinhamento dos botões;
* comportamento das linhas.

O comportamento correto é:

* até aproximadamente 1024px os botões devem permanecer na mesma linha;
* os elementos devem diminuir proporcionalmente;
* NÃO pode quebrar linha para baixo;
* quero um layout fluido e organizado;
* revise visualmente tudo e ajuste qualquer detalhe estranho.

Analise o CSS inteiro e revise possíveis:

* overflows;
* quebras inesperadas;
* desalinhamentos;
* problemas de flex/grid;
* padding e margin inconsistentes.

──────────────────────────────
AUTENTICAÇÃO OBRIGATÓRIA
──────────────────────────────

Agora precisamos implementar a lógica definitiva de autenticação.

REGRAS:

* qualquer pessoa que acessar o Database precisa autenticar primeiro;
* sem autenticação → não acessa o Database;
* se estiver autenticado → acesso liberado;
* autenticação deve persistir por até 7 dias;
* após 7 dias → sessão expira automaticamente;
* remover cache/sessão/token após expiração;
* manter login salvo entre recarregamentos;
* utilizar persistência segura.

Fluxo esperado:

1. usuário acessa:
   database.kendricknicoleti.com

2. sistema verifica autenticação;

3. se NÃO autenticado:
   → redireciona para login;

4. após login:
   → redireciona automaticamente para o Database;

5. se já autenticado:
   → entra direto.

──────────────────────────────
CALENDÁRIO / BOTÃO CONECTAR
──────────────────────────────

A mesma lógica deve funcionar no calendário.

Exemplo:

* usuário clica em “Conectar”;
* sistema verifica login;
* se não autenticado → login;
* autenticou → volta automaticamente para o calendário.

──────────────────────────────
SEPARAÇÃO DOS TÚNEIS CLOUDFLARE
──────────────────────────────

Teremos DOIS túneis separados:

1. TÚNEL RAIZ
   Domínio:
   kendricknicoleti.com

Responsável pelo site principal.

2. TÚNEL DATABASE
   Subdomínio:
   database.kendricknicoleti.com

Responsável exclusivamente pelo Database.

IMPORTANTE:
Os arquivos continuarão na mesma máquina/projeto, porém usando túneis independentes.

Objetivo:

* isolamento;
* estabilidade;
* independência entre serviços;
* manutenção separada.

Exemplo:

* se o túnel principal cair → Database continua funcionando;
* se o túnel Database cair → site principal continua funcionando.

──────────────────────────────
CLOUDFLARE TUNNEL
──────────────────────────────

Configure tudo necessário:

* criação dos dois túneis;
* arquivos de configuração;
* serviços separados;
* credenciais;
* rotas;
* DNS;
* systemd/services;
* estrutura organizada.

O domínio: database.kendricknicoleti.com, deve apontar exclusivamente para: site/database/index.html, usando o túnel Database.

Já o domínio raiz: kendricknicoleti.com, continua usando o túnel principal.

──────────────────────────────
SISTEMAS COMPARTILHADOS
──────────────────────────────

Os dois túneis devem compartilhar:

* sistema de redirecionamento de URLs;
* sistema de páginas de erro;
* lógica de fallback;
* tratamento de erros;
* páginas customizadas.

Tudo deve funcionar igualmente nos dois túneis.

──────────────────────────────
OBJETIVO FINAL
──────────────────────────────

Quero deixar toda a estrutura pronta para produção:

* responsividade revisada;
* autenticação obrigatória;
* persistência de login por 7 dias;
* túneis separados;
* Cloudflare configurado;
* segurança organizada;
* redirecionamentos funcionando;
* páginas de erro funcionando;
* Database isolado do site principal, mas a extrutura de pages continua como esta;
* tudo preparado para deploy final.

──────────────────────────────
COMPACTAÇÃO DE ARQUIVOS / PERFORMANCE
──────────────────────────────

Agora precisamos revisar urgentemente o sistema de compactação de arquivos.

Problemas atuais encontrados:

* quando muitos arquivos são compactados;
* ou quando os arquivos são maiores;
* o sistema fica extremamente lento;
* a compactação demora demais;
* em alguns momentos o sistema “cracha”;
* também está acontecendo algo parecido com negação de serviço (DoS/falso travamento).

Preciso que você investigue profundamente isso.

Analise:

* gargalos de CPU;
* consumo excessivo de RAM;
* loops bloqueando a thread principal;
* problemas de buffer;
* excesso de leitura simultânea;
* escrita temporária;
* problemas no streaming;
* timeout;
* limite do Flask/Gunicorn/Nginx;
* limite do Cloudflare;
* problemas de upload/download;
* compressão síncrona bloqueando processamento;
* múltiplas requisições simultâneas;
* deadlocks;
* vazamento de memória;
* arquivos temporários não removidos;
* possíveis problemas de chunk;
* cache excessivo;
* compressão inteira carregando tudo na memória.

Verifique principalmente se:

* os arquivos estão sendo carregados completamente na RAM;
* o ZIP está sendo montado de forma ineficiente;
* existe bloqueio do event loop;
* existe limite causando falso erro de negação de serviço;
* o Cloudflare está interpretando como tráfego abusivo;
* há rate limit involuntário;
* existe timeout entre túnel ↔ servidor.

──────────────────────────────
OBJETIVO DA OTIMIZAÇÃO
──────────────────────────────

Quero que a compactação:

* suporte múltiplos arquivos grandes;
* funcione rapidamente;
* utilize streaming quando necessário;
* reduza uso de memória;
* evite travamentos;
* evite crash;
* evite falso DoS;
* mantenha estabilidade mesmo com arquivos pesados;
* funcione bem no túnel Cloudflare;
* mantenha o servidor responsivo durante compressão.

Se necessário:

* refatore a lógica de compactação;
* implemente processamento assíncrono;
* utilize fila/background task;
* utilize compressão incremental;
* utilize streaming ZIP;
* implemente limites inteligentes;
* melhore timeout e buffer;
* reorganize upload/download.

Também revise logs e tente identificar exatamente o motivo do crash.
