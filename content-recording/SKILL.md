---
name: content-recording
description: "Planejamento e orientacao de gravacao de videos para midias sociais. Organiza takes, orienta sobre iluminacao, enquadramento e equipamentos. Gera checklist de gravacao e guias por cena. Use quando: planejar gravacao, organizar takes, checklist de equipamento, orientar iluminacao, preparar cenas, listar gravacoes pendentes."
---

# Content Recording

## Onboarding Interativo

Ao iniciar uma sessao de gravacao, pergunte ao usuario:

1. **Roteiro** — Qual roteiro vai gravar? Sugira arquivos de `~/conteudo/campanhas/{cliente}/{tipo}/roteiros/`
2. **Equipamento** — Qual equipamento disponivel? (celular, camera, microfone, ring light, etc.)
3. **Local** — Onde vai gravar? (estudio, casa, externo)
4. **Tomadas** — Quantas tomadas quer de cada cena? (padrao: 3)
5. **Equipe** — Tem auxiliar de gravacao ou vai solo?

Com base nas respostas, gere o checklist e o plano de gravacao.

---

## Checklist de Pre-Gravacao

Gere automaticamente com base no roteiro e nas respostas do onboarding:

- [ ] Roteiro impresso ou visivel no teleprompter
- [ ] Celular/camera carregado (minimo 50% de bateria)
- [ ] Armazenamento disponivel (minimo 5GB livre)
- [ ] Microfone testado (ouvir playback de teste)
- [ ] Iluminacao configurada (luz principal + preenchimento)
- [ ] Fundo/props prontos
- [ ] Modo aviao ativado (evitar interrupcoes)
- [ ] Timer de gravacao configurado
- [ ] Molde de cena no chao (fita adesiva para marcar posicao)
- [ ] Agua e material de apoio na mao

Adicione itens especificos conforme o tipo de equipamento e local informados.

---

## Orientacoes por Tipo de Cena

### Talking Head

- Enquadramento: busto ou cintura, camera na altura dos olhos
- Olhar sempre para a camera (nao para a tela do celular)
- Luz principal a 45 graus do rosto, luz de preenchimento no lado oposto
- Evitar contraluz e janelas ao fundo
- Manter expressao natural, pausar entre frases
- Gravar com temporizador de 3s para estabilizar antes de falar

### B-Roll

- Movimentos suaves e lentos (sem trepidacao)
- Variedade de angulos: frontal, lateral, close, angular
- Duracao minima de 5s por clip (facilita edicao)
- Foco manual para evitar ruidos de AF
- Usar gimbal ou estabilizador quando possivel
- Capturar detalhes e texturas (maos, produtos, ambiente)

### Unboxing / Produto

- Mesa ou superficie limpa e neutra
- Luz uniforme, sem sombras duras
- Close-ups dos detalhes, embalagem, logos
- Mostrar o produto de diferentes angulos
- Gravar reacoes genuinas ao abrir
- Capturar sons ambientes (embalagem rasgando, etc.)

### Screen Recording

- Resolucao 1080p minimo
- Cursor visivel e dimensionado para leitura
- Destacar zonas de foco com bordas ou cor
- Limpar area de trabalho antes de gravar
- Desativar notificacoes do sistema
- Velocidade de navegacao controlada (nao muito rapido)

---

## Plano de Gravacao

Gere um plano de gravacao a partir do roteiro. Formato:

```markdown
# Plano de Gravacao: [Titulo]
- **Data**: YYYY-MM-DD
- **Roteiro**: [caminho ou link]
- **Local**: [local]
- **Duracao estimada**: [XX min]
- **Equipamento**: [lista]
- **Responsavel**: [nome]

## Cena 1: [descricao breve]
- Take 1: □
- Take 2: □
- Take 3: □
- Notas: [orientacao especifica - enquadramento, luz, texto]

## Cena 2: [descricao breve]
- Take 1: □
- Take 2: □
- Take 3: □
- Notas: [orientacao especifica]

## Notas Gerais
- [observacoes do diretor/roteirista]
- [referencias visuais]
```

Salve o plano em:
```
~/conteudo/campanhas/{cliente}/{tipo}/roteiros/plano_{titulo}.md
```

---

## Pos-Gravacao

Apos concluir a gravacao, execute:

1. **Listar arquivos** — Liste todos os arquivos em `brutos/` da campanha
2. **Renomear arquivos** — Padronize nomes: `cena{N}_take{M}.{ext}` (ex: `cena01_take01.mp4`)
3. **Atualizar plano** — Marque os takes realizados com [x] no plano de gravacao
4. **Sinalizar melhores takes** — Flag os takes com asterisco: `cena01_take02*.mp4`
5. **Organizar pastas** — Mova arquivos para estrutura de edicao
6. **Preparar proxima fase** — Indique arquivos prontos para edicao no workflow

Estrutura de saida sugerida:
```
~/conteudo/campanhas/{cliente}/{tipo}/
├── brutos/
│   ├── cena01_take01.mp4
│   ├── cena01_take02*.mp4  (melhor take)
│   └── cena02_take01.mp4
├── roteiros/
│   └── plano_{titulo}.md
└── editados/
```

---

## Referencias

Consulte `references/equipment_guide.md` para recomendacoes de equipamento por faixa de preco.
