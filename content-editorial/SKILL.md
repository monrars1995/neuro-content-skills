---
name: content-editorial
description: "Criacao de calendarios editoriais e linhas editoriais para midias sociais. Define pilares de conteudo, tematicas recorrentes, calendario de publicacao e estrategia de conteudo por cliente. Gera plano mensal/semanal integrado com trends e metricas. Use quando: criar calendario editorial, criar linha editorial, planejar conteudo mensal, definir pilares de conteudo, tematicas recorrentes, estrategia de conteudo, agenda de posts. Comandos: /create-editorial, /create-linha-editorial."
---

# Content Editorial - Linha Editorial e Calendario

## Slash Commands

### `/create-linha-editorial [cliente]` - Criar Linha Editorial

Aciona quando usuario digita `/create-linha-editorial` ou `/create-linha-editorial <cliente>`.

Define a identidade estrategica de conteudo de um cliente. Responde: O QUE falar, PARA QUEM, COMO e QUANDO.

**Onboarding Interativo:**

1. Se cliente nao fornecido, listar disponiveis e pedir selecao
2. Carregar contexto existente do cliente (content-memory)
3. Se contexto existe, perguntar: "Ja existe uma linha editorial. Deseja atualizar ou criar nova?"
4. Se nova ou atualizar, iniciar definicoes:

**Fase 1: Identidade**
- "Qual a missao do conteudo?" (o que o conteudo deve comunicar)
- "Quais os pilares de conteudo?" (3-5 temas centrais)
  - Exemplo fitness: Treino, Nutricao, Motivacao, Dicas, Bastidores
  - Exemplo finanzas: Educacao financeira, Investimentos, Economia, Metas, Cases
- "Qual o posicionamento?" (autoridade, proximo, inspirador, provocativo)
- "Quais os temas recorrentes?" (series semanais, rubricas fixas)

**Fase 2: Formato**
- "Quais formatos de video?" (talking head, tutorial, b-roll, mashup, POV, trend)
- "Qual a distribuicao por tipo?" (ex: 40% educativo, 30% entretenimento, 30% vendas)
- "Qual a duracao padrao?" (15s, 30s, 60s, variado)

**Fase 3: Calendario Base**
- "Quais dias da semana publicar?" (seg-sex, todos os dias, etc.)
- "Quais horarios?" (com base em metricas se disponivel)
- "Tem datas sazonais importantes?" (black friday, natal, datas do nicho)

**Gerar documento de Linha Editorial:**

Salvar em `~/conteudo/campanhas/{cliente}/briefings/linha_editorial.md`:

```markdown
# Linha Editorial - {cliente}

## Identidade
- **Missao do conteudo**: {missao}
- **Posicionamento**: {posicionamento}
- **Tom de voz**: {tom}

## Pilares de Conteudo
### 1. {pilar} ({percentual}%)
- Objetivo: {o que comunicar}
- Formatos ideais: {formatos}
- Exemplos de temas: {exemplos}
- CTA principal: {cta}

### 2. {pilar} ({percentual}%)
...

## Temas Recorrentes
| Serie | Frequencia | Dia da semana | Descricao |
|-------|-----------|---------------|-----------|
| {nome} | {semanal/mensal} | {dia} | {descricao} |

## Formatos e Distribuicao
| Formato | % do conteudo | Duracao | Frequencia |
|---------|--------------|---------|-------------|
| {formato} | {xx}% | {xx}s | {xx}x/semana |

## Calendario Semanal Base
| Dia | Horario | Pilar | Formato | Tema |
|-----|---------|-------|---------|------|
| Seg | {hh:mm} | {pilar} | {formato} | {tema} |
| Ter | {hh:mm} | {pilar} | {formato} | {tema} |
...

## Datas Sazonais
| Data | Evento | Pilar | Antecedencia |
|------|--------|-------|-------------|
| {data} | {evento} | {pilar} | {xx} dias antes |
```

**Pos-criacao:**
- Atualizar contexto.json com os pilares e distribuicao
- Salvar como story: "Linha editorial criada/ atualizada"
- Perguntar: "Deseja gerar o calendario editorial mensal agora? (/create-editorial)"

### `/create-editorial [cliente] [mes]` - Criar Calendario Editorial

Aciona quando usuario digita `/create-editorial` ou `/create-editorial <cliente> <mes>`.

Gera o calendario de conteudo mensal com base na linha editorial e trends atuais.

**Onboarding Interativo:**

1. Se cliente nao fornecido, listar disponiveis
2. Se mes nao fornecido, usar mes atual
3. Carregar linha editorial do cliente (briefings/linha_editorial.md)
4. Se nao existe linha editorial, sugerir: "Nenhuma linha editorial encontrada. Deseja criar primeiro? (/create-linha-editorial)"
5. Perguntar:
   - "Deseja integrar trends atuais no calendario?" (sim/nao)
   - "Quantos posts por semana?" (usar padrao da linha editorial)
   - "Tem algum tema ou campanha especifica este mes?"
   - "Deseja gerar ideias para todos os posts ou apenas a estrutura?"

**Workflow de Geracao:**

1. Buscar trends atuais se solicitado (content-ideas)
2. Buscar metricas de performance do mes anterior (content-metrics)
3. Identificar datas sazonais do mes
4. Distribuir pilares conforme porcentagem da linha editorial
5. Alinhar formatos por dia da semana
6. Sugerir temas especificos para cada post
7. Gerar calendario completo

**Gerar documento de Calendario Editorial:**

Salvar em `~/conteudo/campanhas/{cliente}/briefings/calendario_{YYYY}_{MM}.md`:

```markdown
# Calendario Editorial - {cliente} - {Mes/Ano}

## Resumo
- **Total de posts**: {X}
- **Posts por semana**: {X}
- **Pilares ativos**: {lista}

## Semana 1 ({dd} a {dd})
| Data | Dia | Horario | Pilar | Formato | Tema | Status |
|------|-----|---------|-------|---------|------|--------|
| {dd} | {dia} | {hh:mm} | {pilar} | {formato} | {tema} | ⬜ Pendente |

## Semana 2 ({dd} a {dd})
...

## Semana 3 ({dd} a {dd})
...

## Semana 4 ({dd} a {dd})
...

## Datas Sazonais do Mes
| Data | Evento | Post Previsto |
|------|--------|---------------|
| {dd} | {evento} | {tema do post} |

## Trend Opportunities
| Trend | Plataforma | Dia sugerido | Pilar |
|-------|-----------|-------------|-------|
| {trend} | {plataforma} | {dia} | {pilar} |

## Observacoes
- {notas sobre estrategia do mes}
```

**Pos-criacao:**
- Perguntar: "Deseja iniciar o pipeline de criacao para algum post do calendario?"
- Se sim, redirecionar para `/nova-campanha` com o tema selecionado
- Salvar referencia no contexto.json

## Templates de Pilares por Nicho

### Fitness
1. Treino e Exercicio (35%)
2. Nutricao e Suplementacao (25%)
3. Motivacao e Mentalidade (20%)
4. Dicas e FAQ (15%)
5. Bastidores e Rotina (5%)

### Finanzas
1. Educacao Financeira (30%)
2. Investimentos e Renda (25%)
3. Economia e Noticias (20%)
4. Metas e Planejamento (15%)
5. Cases e Resultados (10%)

### Gastronomia
1. Receitas e Tutoriais (40%)
2. Dicas e Tecnicas (25%)
3. Reviews e Avaliacoes (15%)
4. Bastidores e Rotina (10%)
5. Trends e Desafios (10%)

### Tecnologia
1. Dicas e Tutoriais (35%)
2. Reviews de Produtos (25%)
3. Noticias e Lançamentos (20%)
4. Comparativos (10%)
5. Bastidores e Setup (10%)

### Moda
1. Looks e Combinacoes (35%)
2. Dicas de Estilo (25%)
3. Haul e Reviews (20%)
4. Trends e Tendencias (15%)
5. Bastidores (5%)

### Educacao
1. Micro-aulas (40%)
2. Dicas de Estudo (25%)
3. Motivacao e Mentalidade (20%)
4. Ferramentas e Apps (10%)
5. Resultados e Cases (5%)

## Referencias

- **Estrutura de pastas**: content-fs
- **Memoria do cliente**: content-memory
- **Pesquisa de trends**: content-ideas
- **Metricas de performance**: content-metrics
- **Criacao de roteiro**: content-script
