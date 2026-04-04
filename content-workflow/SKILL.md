---
name: content-workflow
description: "Orquestrador principal do pipeline de criacao de conteudo para midias sociais. Coordena todas as etapas: Planejamento Editorial, Ideias, Roteiro, Gravacao, Edicao (Remotion), Publicacao (TikTok/Instagram) e Metricas. Gerencia multiplos clientes, memoria persistente e estrutura de pastas. Use quando: criar conteudo, pipeline de video, campanha de midia social, workflow de conteudo, onboarding de cliente, status de campanha, gerenciar clientes, fluxo completo de criacao de conteudo, iniciar projeto, setup inicial. Comandos: /iniciar-projeto, /cliente-setup, /nova-campanha, /status, /continuar."
---

# Content Workflow - Pipeline Completo de Criacao de Conteudo

Orquestra o pipeline de 7 etapas para criacao de conteudo em midias sociais.

## Comportamento do Agente

### Principios de Interacao

1. **Sempre fale em PT-BR** com o usuario. Toda comunicacao, feedback, perguntas e orientacoes devem ser em portugues brasileiro.
2. **Um passo por vez.** Nunca pule etapas nem faca multiplas perguntas de uma vez. Execute cada passo, confirme com o usuario, e so entao avance.
3. **Confirme antes de criar/alterar arquivos.** Sempre mostre ao usuario o que vai ser criado e peça confirmacao antes de executar comandos que criem, movam ou excluam arquivos.
4. **Exiba progresso visual.** Use indicadores de progresso (ex: "Etapa 1/5", "Criando pastas... OK") para que o usuario saiba onde esta.
5. **Ofereça opcoes quando houver ambiguidade.** Em vez de perguntar aberto, ofereca lista numerada de opcoes quando possivel.
6. **Sempre valide apos criar.** Apos criar qualquer arquivo, confirme que foi criado com sucesso. Apos criar pastas, liste-as. Apos criar JSON, valide-o.
7. **Use markdown formatado.** Use bold, listas, tabelas e blocos de codigo para melhor legibilidade.
8. **Mantenha contexto entre comandos.** Se o usuario acabou de configurar algo, nao pergunte de novo. Lembre do que ja foi feito na sessao.
9. **Em caso de erro, explique e sugira solucao.** Nunca falhe silenciosamente. Explique o que deu errado e ofereca proximos passos.
10. **Ao finalizar uma acao, sugira o proximo comando.** Ex: "Pronto! Agora voce pode usar `/create-linha-editorial` para definir a estrategia de conteudo."

### Formato de Respostas

- Mensagens curtas e diretas
- Usar tabelas para informacoes estruturadas
- Usar blocos de codigo para comandos
- Usar emoji apenas em indicadores de status (opcional)
- Nunca use mais de 3 paragrafos seguidos sem interagir com o usuario

## Etapas do Pipeline

```
0. PLANEJAMENTO EDITORIAL (content-editorial)
   ↓
1. IDEIAS (content-ideas)
   ↓
2. ROTEIRO (content-script)
   ↓
3. GRAVACAO (content-recording)
   ↓
4. EDICAO (content-editing)
   ↓
5. PUBLICACAO (content-publishing)
   ↓
6. METRICAS (content-metrics)
```

## Skills do Pacote

| Skill | Funcao | Trigger |
|-------|--------|---------|
| content-fs | Estrutura de pastas e organizacao de midia | Criar campanha, organizar arquivos |
| content-memory | Memoria persistente e contexto do cliente | Lembrar preferencias, historico |
| content-editorial | Linha editorial e calendario de conteudo | Criar calendario, planejar conteudo |
| content-ideas | Pesquisa de trends e captacao de ideias | Buscar ideias, trends |
| content-script | Roteirizacao Hook-Desenvolvimento-CTA | Criar roteiro, script |
| content-recording | Planejamento de gravacao | Preparar gravacao, takes |
| content-editing | Edicao de video com Remotion | Editar video, montar, legendas |
| content-publishing | Publicacao via TikTok/Instagram API | Publicar, agendar |
| content-metrics | Analise de performance | Metricas, relatorios |

## Slash Commands

### `/iniciar-projeto` - Setup Completo do Workspace

Aciona quando usuario digita `/iniciar-projeto`.

Este e o comando principal de entrada. Configura tudo do zero: workspace, primeiro cliente, APIs e primeiras acoes.

**Fluxo de Execucao:**

```
ETAPA 1/5: Workspace
├── Verificar se ~/conteudo existe
├── Se nao existe, criar e configurar
└── Mostrar estrutura criada

ETAPA 2/5: Primeiro Cliente
├── Perguntar nome do cliente (slug, ex: joao-academia)
├── Perguntar nicho (com sugestoes)
├── Perguntar plataformas (com checkboxes)
├── Perguntar tom de voz
├── Perguntar frequencia de publicacao
└── Criar estrutura completa de pastas

ETAPA 3/5: Memoria e Config
├── Inicializar contexto.json com dados do cliente
├── Inicializar historico.json vazio
├── Criar .env.cliente vazio
├── Criar .gitignore com .env.cliente
└── Validar tudo com validate_schema.py

ETAPA 4/5: APIs (opcional)
├── Perguntar quais APIs configurar agora
├── Se TikTok: guiar setup completo
├── Se Instagram: guiar setup completo
├── Se nenhuma: explicar que pode configurar depois
└── Testar conexoes configuradas

ETAPA 5/5: Primeiras Acoes
├── Sugerir proximos passos com links para comandos
├── Oferecer criar linha editorial agora
└── Mostrar resumo final do setup
```

**Detalhamento por etapa:**

**ETAPA 1/5: Workspace**

Execute:
```bash
mkdir -p ~/conteudo
mkdir -p ~/conteudo/referencias/{trends,templates}
mkdir -p ~/conteudo/assets/{musicas,fontes,overlays}
```

Confirme:
```
Workspace criado em ~/conteudo/
```

**ETAPA 2/5: Primeiro Cliente**

Pergunte de forma estruturada:

> **Vamos configurar seu primeiro cliente!**
>
> **1. Nome do cliente** (use slug, ex: `joao-academia`, `maria-financas`):
>
> **2. Nicho/segmento:**
> - fitness
> - financas/investimentos
> - gastronomia
> - tecnologia
> - moda/beleza
> - educacao
> - imobiliario
> - saude
> - outro: _______
>
> **3. Plataformas de publicacao:**
> - [ ] TikTok
> - [ ] Instagram Reels
> - [ ] YouTube Shorts
> - [ ] Todas
>
> **4. Tom de voz:**
> - educativo
> - humoristico
> - inspiracional
> - provocativo
> - vendas/direto
> - outro: _______
>
> **5. Frequencia de publicacao:**
> - diaria
> - 3x por semana
> - semanal
> - quinzenal

Apos coletar, execute `ensure_client_dirs` do content-fs e inicialize os JSONs:

```bash
CLIENTE="nome-digitado"
BASE=~/conteudo/campanhas/$CLIENTE

mkdir -p "$BASE"/{posts-midias-sociais/{ideias,roteiros,brutos,editados,publicados}}
mkdir -p "$BASE"/{criativos-anuncios/{ideias,roteiros,brutos,editados,publicados}}
mkdir -p "$BASE"/{briefings,metricas}

echo '{"cliente":{"nome":"NOME","nicho":"NICHO","plataformas":[],"tom_de_voz":"","cta_padrao":"","horarios_melhores":[]},"preferencias":{},"stories":[],"metricas_resumo":{"total_publicados":0,"avg_retention":"0%","avg_engagement":"0%","melhor_horario":"","ultima_atualizacao":""}}' > "$BASE/contexto.json"

echo '{"entries":[]}' > "$BASE/historico.json"

touch "$BASE/.env.cliente"
```

Valide:
```bash
python3 ~/.opencode/skills/content-memory/scripts/validate_schema.py --cliente "$CLIENTE"
```

Confirme estrutura criada listando as pastas.

**ETAPA 3/5: Memoria e Config**

Preencher o contexto.json com os dados coletados na etapa anterior. Atualizar os campos:
- `cliente.nome`
- `cliente.nicho`
- `cliente.plataformas`
- `cliente.tom_de_voz`
- `cliente.cta_padrao` (sugira com base no nicho)
- `cliente.horarios_melhores` (sugira com base em metricas do nicho)

Garantir .gitignore:
```bash
if [ -f ~/conteudo/.gitignore ]; then
  grep -qxF '.env.cliente' ~/conteudo/.gitignore || echo '.env.cliente' >> ~/conteudo/.gitignore
else
  echo '.env.cliente' > ~/conteudo/.gitignore
fi
```

**ETAPA 4/5: APIs (opcional)**

Pergunte:
> **Deseja configurar as APIs de publicacao agora?**
>
> - [ ] TikTok (Content Posting API)
> - [ ] Instagram (Graph API)
> - [ ] Nenhuma por agora (posso configurar depois com `/setup-api`)

Se TikTok selecionado, guiar passo a passo:
1. Acesse https://developers.tiktok.com
2. Crie conta de desenvolvedor
3. Crie um App no dashboard
4. Ative "Content Posting" nas APIs
5. Gere Access Token com scopes: `video.upload`, `video.publish`
6. Cole o token abaixo:
7. Cole o App ID abaixo:
8. Cole o username do perfil TikTok abaixo:

Se Instagram selecionado, guiar passo a passo:
1. Acesse https://developers.facebook.com
2. Crie um App (tipo Business)
3. Adicione Instagram Basic Display API
4. Vincule a Pagina do Facebook
5. Ative Content Publishing
6. Gere Long-lived Access Token
7. Obtenha Instagram Business Account ID
8. Cole os dados abaixo:

Apos coletar, salvar no `.env.cliente` e confirmar.

**ETAPA 5/5: Primeiras Acoes**

Exiba resumo final:

> **Setup concluido!**
>
> ```
> Workspace: ~/conteudo/
> Cliente: {nome} ({nicho})
> Plataformas: {plataformas}
> Pasta: ~/conteudo/campanhas/{nome}/
> APIs: {status das APIs}
> ```
>
> **Proximos passos sugeridos:**
> 1. `/create-linha-editorial {nome}` - Definir estrategia de conteudo
> 2. `/create-editorial {nome}` - Gerar calendario mensal
> 3. `/trends {nome}` - Pesquisar trends do nicho
> 4. `/nova-campanha {nome}` - Iniciar pipeline de conteudo
> 5. `/status` - Ver painel de status

### `/cliente-setup [nome]` - Onboarding de Cliente Adicional

Aciona quando usuario digita `/cliente-setup` ou `/cliente-setup <nome>`.

Semelhante a Etapa 2-4 do `/iniciar-projeto`, mas para clientes adicionais.
Assume que o workspace ja existe.

1. Se nome nao fornecido, perguntar
2. Verificar se cliente ja existe em ~/conteudo/campanhas/
3. Se existe, perguntar se deseja atualizar
4. Se novo, executar onboarding interativo (mesmo fluxo do iniciar-projeto etapas 2-4)
5. Resumo final

### `/nova-campanha [cliente]` - Iniciar Pipeline de Conteudo

Aciona quando usuario digita `/nova-campanha` ou `/nova-campanha <cliente>`.

1. Se cliente nao fornecido, listar clientes disponiveis e pedir selecao
2. Carregar contexto do cliente (content-memory)
3. Exibir resumo do cliente em tabela
4. Perguntar tipo de conteudo com opcoes numeradas
5. Confirmar e iniciar pipeline na etapa 0 (Planejamento Editorial)
6. A cada etapa concluida, perguntar: "Deseja avancar para a proxima etapa?"

### `/status` - Painel de Status

Aciona quando usuario digita `/status`.

1. Escanear ~/conteudo/campanhas/ para todos os clientes
2. Para cada cliente, exibir painel formatado:
   ```
   {cliente} ({nicho})
   ├── Ideias pendentes: X
   ├── Roteiros prontos: X
   ├── Brutos: X
   ├── Editados prontos: X
   ├── Publicados esta semana: X
   ├── Metricas: X% engajamento | X% retencao
   └── Etapa atual: [etapa]
   ```
3. Sugerir proximas acoes por cliente
4. Destacar clientes sem atividade recente (>7 dias)

### `/continuar [cliente]` - Retomar Pipeline

Aciona quando usuario digita `/continuar` ou `/continuar <cliente>`.

1. Se cliente nao fornecido, listar clientes com pipeline ativo
2. Carregar contexto do cliente
3. Identificar ultima etapa concluida via historico.json
4. Resumir o que ja foi feito
5. Perguntar: "Deseja retomar de [proxima etapa]?"
6. Se sim, iniciar workflow dessa etapa

## Fluxo de Uma Campanha

### Etapa 0: Planejamento Editorial
- Verificar se existe linha editorial para o cliente (content-editorial)
- Se nao existe, sugerir `/create-linha-editorial`
- Se existe, carregar calendario editorial atual
- Alinhar conteudo do pipeline com o calendario

### Etapa 1: Ideias
- Carregar trends recentes (content-ideas)
- Analisar concorrentes via Meta Ads Library
- Gerar 5-10 ideias com base em trends + nicho
- Salvar ideias aprovadas

### Etapa 2: Roteiro
- Selecionar ideia aprovada
- Gerar roteiro Hook-Desenvolvimento-CTA
- Ajustar tom e duracao
- Salvar roteiro

### Etapa 3: Gravacao
- Gerar plano de gravacao a partir do roteiro
- Checklist de equipamento e preparacao
- Apos gravacao: organizar arquivos brutos

### Etapa 4: Edicao
- Selecionar melhores takes
- Montar no Remotion com template
- Aplicar legendas e overlays
- Exportar video final

### Etapa 5: Publicacao
- Gerar metadata (descricao, hashtags)
- Publicar nas plataformas configuradas
- Salvar registro de publicacao

### Etapa 6: Metricas
- Coletar metricas apos 24h/48h/7d
- Analisar retencao e engajamento
- Gerar insights
- Salvar aprendizados (stories) no contexto

## Regras

- Sempre carregar contexto do cliente antes de qualquer acao
- Sempre salvar aprendizados apos cada publicacao
- Sempre perguntar antes de avancar etapa
- Sempre respeitar a estrutura de pastas padrao
- Nunca publicar sem preview/approvacao do usuario
- Nunca commitar arquivos .env.cliente
- Sempre validar JSON apos criar/editar (use jq ou validate_schema.py)
- Sempre sugerir o proximo comando ao finalizar uma acao
