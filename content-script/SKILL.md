---
name: content-script
description: "Roteirizacao de videos para midias sociais com framework Hook-Desenvolvimento-CTA. Cria roteiros estruturados com gancho nos primeiros 3 segundos, desenvolvimento do conteudo e chamada para acao. Use quando: criar roteiro, escrever script de video, estruturar video, criar hook, escrever CTA, planejar conteudo."
---

# Content Script - Roteirizacao de Videos

## Framework de Roteirizacao

Todo roteiro segue a estrutura: **Hook (3s) -> Desenvolvimento -> CTA**

### HOOK (0-3 segundos)

O hook determina se o usuario continua assistindo. Deve gerar urgencia ou impossibilidade de nao continuar.

**Tipos de hook:**

- **Pergunta impactante**: Questiona algo que o publico acredita ser verdade
- **Dado chocante**: Apresenta estatistica ou numero surpreendente
- **Promessa ousada**: Garante resultado transformador
- **Contradicao**: Afirma o oposto do senso comum
- **Curiosidade gap**: Apresenta informacao incompleta que gera curiosidade

Consulte `references/hooks_library.md` para exemplos por nicho.

### DESENVOLVIMENTO (3s - final)

- Mantenha ritmo acelerado, cortes a cada 2-3 segundos
- Use storytelling: Situacao -> Conflito -> Resolucao
- Texto na tela complementa (nao repete) o audio
- Inclua transicoes e mudancas de cena a cada 5-8 segundos
- Evite pausas longas ou explicacoes excessivas
- Cada cena deve ter: fala + visual + texto na tela

### CTA (ultimos 3-5 segundos)

- Tipos: Siga, Comente, Salve, Compartilhe, Link na bio
- Deve ser natural e conectado ao conteudo
- Evite CTAs genericos; personalize com base no video
- O CTA deve fazer sentido como continuacao natural do conteudo

## Onboarding Interativo

Ao criar um roteiro, pergunte:

1. Qual a ideia/tema do video? (se ja tiver ideia salva, sugira do banco)
2. Qual a duracao alvo? (15s, 30s, 60s, 90s)
3. Qual o tom? (educativo, humor, inspiracional, vendas)
4. Qual o CTA principal?
5. Ja tem conteudo bruto gravado ou vai gravar depois?

## Template de Roteiro

Salve roteiros em `~/conteudo/campanhas/{cliente}/{tipo}/roteiros/`.

Crie o diretorio se nao existir:
```bash
mkdir -p ~/conteudo/campanhas/{cliente}/{tipo}/roteiros/
```

Formato `.md`:

```markdown
# Roteiro: [Titulo]
- **Idea base**: [link para idea]
- **Duracao alvo**: [XXs]
- **Tom**: [tipo]
- **Plataformas**: [lista]

## HOOK (0-3s)
[Fala] ...
[Visual] ...
[Texto na tela] ...

## DESENVOLVIMENTO
### Cena 1 (3-8s)
[Fala] ...
[Visual] ...
[Texto na tela] ...

### Cena 2 (8-15s)
[Fala] ...
[Visual] ...
[Texto na tela] ...

## CTA (final)
[Fala] ...
[Visual] ...
```

## Script Enhancement

Apos gerar o roteiro, execute a verificacao:

### 1. Forca do Hook (1-10)

- 9-10: Impossivel nao continuar. Gera reacao imediata.
- 7-8: Bom, prende atencao na maioria dos casos.
- 5-6: Funciona, mas pode ser mais forte.
- Abaixo de 5: Reescrever. Nao vai reter o publico.

### 2. CTA Especifico

- O CTA e generico? Refaca com contexto do video.
- O CTA conecta naturalmente ao conteudo?
- O CTA pede uma unica acao clara?

### 3. Duracao

- Conte as palavras faladas (~150 palavras/min para ritmo acelerado)
- Verifique se o numero de cenas condiz com a duracao
- Ajuste se necessario

### 4. Hooks Alternativos

Gere 2 opcoes alternativas de hook para o mesmo roteiro, usando tipos diferentes do hook original. Apresente ao usuario para escolha.

## Fluxo de Trabalho

1. Verifique se ha ideias salvas em `~/conteudo/campanhas/{cliente}/posts-midias-sociais/ideias/`
2. Se houver, sugira ideias disponiveis
3. Colete as respostas do onboarding
4. Gere o roteiro seguindo o template
5. Execute o script enhancement
6. Salve o roteiro final
