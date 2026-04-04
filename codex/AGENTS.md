Voce tem acesso a um pipeline completo de criacao de conteudo para midias sociais com 10 skills especializadas.

## Comandos disponiveis

### Setup e Gestao
- `/iniciar-projeto` - Setup completo do workspace e primeiro cliente (COMECE AQUI)
- `/cliente-setup [nome]` - Onboarding de cliente adicional
- `/status` - Painel de status de todos os clientes
- `/continuar [cliente]` - Retomar pipeline interrompido

### Planejamento e Ideias
- `/create-linha-editorial [cliente]` - Definir estrategia e pilares de conteudo
- `/create-editorial [cliente]` - Gerar calendario mensal de publicacao
- `/trends [cliente]` - Pesquisar trends do nicho (TikTok, Google, Meta)
- `/ideias [cliente]` - Gerar ideias de conteudo baseadas em trends
- `/concorrentes [cliente]` - Analisar anuncios de concorrentes

### Criacao
- `/roteiro [cliente]` - Criar roteiro de video (Hook-Desenvolvimento-CTA)
- `/hook` - Gerar hooks alternativos para um roteiro
- `/cta` - Gerar CTAs alternativos
- `/gravar [cliente]` - Planejar sessao de gravacao
- `/plano-gravacao [cliente]` - Gerar plano detalhado de gravacao
- `/checklist [cliente]` - Checklist de pre-gravacao

### Edicao
- `/editar [cliente]` - Editar video com Remotion
- `/legendas [video] [cliente]` - Gerar legendas automaticas (Whisper/OpenAI)
- `/render [cliente] - Renderizar video final
- `/template [cliente]` - Listar/gerar templates de edicao

### Publicacao e Metricas
- `/publicar [cliente]` - Publicar nas plataformas
- `/agendar [cliente] - Agendar publicacao
- `/setup-api [cliente]` - Configurar APIs de publicacao
- `/metricas [cliente]` - Analisar metricas de performance
- `/relatorio [cliente] - Gerar relatorio completo
- `/insights [cliente]` - Insights e recomendacoes

### Memoria
- `/lembrar [cliente]` - Consultar contexto do cliente
- `/historico [cliente]` - Ver historico de publicacoes
- `/stories [cliente]` - Consultar aprendizados salvos
- `/contexto [cliente]` - Ver resumo completo do cliente

## Workspace

- Raiz: ~/conteudo
- Clientes: ~/conteudo/campanhas/{cliente}/
- Referencias: ~/conteudo/referencias/
- Assets: ~/conteudo/assets/

## Regras de Comportamento

- SEMPRE fale em PT-BR com o usuario
- Um passo por vez - nunca pule etapas
- Confirme antes de criar/alterar arquivos
- Valide JSON apos criar/editar
- Nunca publique sem aprovacao do usuario
- Nunca commite .env.cliente
- Ao finalizar, sugira o proximo comando

## Pipeline de Conteudo

```
0. Planejamento Editorial
1. Ideias (trends + nicho)
2. Roteiro (Hook-Desenvolvimento-CTA)
3. Gravacao (plano + checklist)
4. Edicao (Remotion + legendas)
5. Publicacao (APIs TikTok/Instagram)
6. Metricas (analise + insights)
```
