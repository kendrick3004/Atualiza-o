# PROMPT OPERACIONAL OBRIGATÓRIO — CLAUDE CODE
> Versão unificada e definitiva. Este documento substitui e consolida todos os prompts anteriores.
> Leia integralmente antes de qualquer ação.

---

## MODO DE OPERAÇÃO

Você está em **modo EXECUÇÃO**, não em modo consultoria.

**Proibições absolutas:**
- NÃO explique o que vai fazer antes de fazer.
- NÃO fique em modo planejamento.
- NÃO descreva ferramentas.
- NÃO procure `package.json` como primeira ação genérica.
- NÃO faça buscas genéricas sem leitura de arquivo específico primeiro.
- NÃO interrompa o trabalho para explicar decisões óbvias.
- NÃO pergunte "posso continuar?", "devo prosseguir?", "quer que eu execute?" — o usuário já autorizou tudo neste documento.

**Obrigações:**
- Mostre ações concretas.
- Mostre arquivos alterados.
- Mostre progresso real e contínuo.
- Execute automaticamente as ações necessárias.
- Baseie TODAS as decisões no que foi lido — nunca em suposições.

---

## PASSO 1 — EXECUÇÃO SOB DEMANDA

Após a varredura, todas as ações seguintes são executadas **somente mediante instrução do usuário**.

Ao receber uma instrução:
1. Baseie-se no mapa construído na varredura — nunca em suposições.
2. Execute a tarefa diretamente, sem explicar antes.
3. Mostre arquivos alterados e o que mudou.
4. Ao terminar, atualize o `README.md` conforme o Passo 3.
5. Confirme o que foi feito e aguarde a próxima instrução.
6. Se identificar um problema fora do escopo da tarefa, registre-o mas não interrompa o fluxo.

---

## PASSO 2 — ATUALIZAÇÃO CONTÍNUA DO README.md

### Regra permanente e obrigatória

**Após cada modificação no projeto — sem exceção — o `README.md` deve ser atualizado automaticamente, sem precisar de instrução.**

Isso inclui: criação de arquivo, edição de arquivo, adição de dependência, mudança de arquitetura, correção de bug, nova funcionalidade, alteração de estrutura de pastas, mudança de tecnologia, ou qualquer outra alteração relevante.

---

### O que o README.md deve conter e manter atualizado

O `README.md` é um documento vivo que reflete o estado real e atual do projeto. Estrutura obrigatória:

**1. Visão Geral**
- O que é o projeto
- Para que serve
- Como funciona em alto nível

**2. Tecnologias Utilizadas**
- Linguagens, frameworks, bibliotecas e ferramentas
- Versões relevantes
- Atualizar sempre que uma nova tecnologia for adicionada ou removida

**3. Estrutura do Projeto**
- Árvore de pastas com descrição de cada diretório e arquivo relevante
- Atualizar sempre que arquivos ou pastas forem criados, movidos ou removidos

```
projeto/
├── .claude/           ← configurações operacionais do Claude Code
├── src/               ← [descrição]
├── README.md          ← este arquivo
└── ...
```

**4. Como Funciona**
- Fluxo principal de execução
- Pontos de entrada do sistema
- Descrição dos módulos principais e suas responsabilidades

**5. Como Rodar / Instalar**
- Pré-requisitos
- Comandos para instalar dependências
- Comandos para executar

**6. Histórico de Modificações**
- Lista cronológica das alterações feitas pelo Claude Code
- Formato:

```
## Modificações

### [YYYY-MM-DD HH:MM]
- O que foi feito
- Arquivos criados/editados
- Motivo da alteração
```

---

### Regras de edição do README

- **Nunca apague seções existentes** — apenas edite e expanda.
- **Nunca substitua o README inteiro** — faça edições cirúrgicas nas seções afetadas.
- **Sempre adicione** a modificação atual no Histórico de Modificações.
- Se o README não existir: crie-o com todas as seções acima preenchidas com base no que foi lido na varredura.
- Se existir mas estiver desatualizado: corrija apenas o que mudou, preservando o restante.

---

## PASSO 3 — ARQUITETURA E QUALIDADE DO CÓDIGO

Todo código criado ou modificado deve ser:
- **Modular**: cada responsabilidade em seu próprio módulo
- **Assíncrono**: sem bloqueio do processo principal onde aplicável
- **Resiliente**: tolerante a falhas em todos os pontos críticos
- **Performático**: sem overhead desnecessário
- **Compatível**: funcionar em Windows e Linux

Cada módulo deve ter documentação inline explicando:
- Responsabilidade do módulo
- Fluxo de execução interno
- Pontos críticos de falha
- Estratégia de tratamento de erros

---

## COMPATIBILIDADE COM SESSÕES ANTERIORES

Ao iniciar, assuma que trabalhos anteriores podem já existir parcialmente. Identifique o que existe, complemente o que falta, e corrija o que estiver incompleto — sem destruir o que já funciona.

---

## RESUMO DA ORDEM DE EXECUÇÃO

```
1. Varredura completa do projeto (ler todos os arquivos, mapear tudo)
2. Exibir resumo da varredura
3. PARAR e aguardar instrução do usuário
4. Executar tarefas sob demanda, baseando-se sempre no mapa construído
5. *** APÓS CADA TAREFA *** atualizar README.md automaticamente
6. Nunca apagar seções do README — apenas editar e expandir
7. Nunca destruir o que já funciona — complementar e corrigir
```

---

*Este documento deve ser mantido em `.claude/PROMPT_OPERACIONAL.md` e relido no início de cada nova sessão do Claude Code.*