# Schemas JSON - content-memory

## contexto.json

Caminho: `~/conteudo/campanhas/{cliente}/contexto.json`

Arquivo central de memoria do cliente. Armazena dados ativos, preferencias, stories e resumo de metricas.

```json
{
  "cliente": {
    "nome": "Nome exibido do cliente",
    "nicho": "Segmento de atuacao (ex: gastronomia, saude, imobiliario)",
    "plataformas": ["instagram", "tiktok", "youtube"],
    "tom_de_voz": "Descricao do tom (ex: descontraido, educativo, inspirador)",
    "cta_padrao": "Chamada para acao padrao (ex: Link na bio, Comente abaixo)",
    "horarios_melhores": ["18:00", "12:00"]
  },
  "preferencias": {
    "duracao_video": "30s",
    "formato_preferido": "reels",
    "estilo_edicao": "dinamico com cortes rapidos",
    "cores_marca": ["#FF5733", "#333333", "#FFFFFF"]
  },
  "stories": [
    {
      "id": "story_20250115143000",
      "data": "2025-01-15",
      "titulo": "Reels com legenda no inicio engajam mais",
      "conteudo": "Testamos 3 reels com legenda nos primeiros 3 segundos vs sem legenda. Os com legenda tiveram 42% mais retencao.",
      "tags": ["reels", "legenda", "retencao"],
      "relevancia": "alta"
    }
  ],
  "metricas_resumo": {
    "total_publicados": 45,
    "avg_retention": "68.3%",
    "avg_engagement": "4.2%",
    "melhor_horario": "18:00",
    "ultima_atualizacao": "2025-01-15"
  }
}
```

### Campos

| Campo | Tipo | Descricao |
|-------|------|-----------|
| cliente.nome | string | Nome de exibicao do cliente |
| cliente.nicho | string | Nicho/segmento do cliente |
| cliente.plataformas | string[] | Lista de plataformas ativas |
| cliente.tom_de_voz | string | Tom de comunicacao preferido |
| cliente.cta_padrao | string | CTA padrao para posts |
| cliente.horarios_melhores | string[] | Horarios com melhor performance (HH:MM) |
| preferencias.duracao_video | string | Duracao ideal de video (ex: 30s, 60s) |
| preferencias.formato_preferido | string | Formato preferido (reels, stories, carrossel) |
| preferencias.estilo_edicao | string | Descricao do estilo de edicao |
| preferencias.cores_marca | string[] | Cores hexadecimais da marca |
| stories[].id | string | Identificador unico (story_YYYYMMDDHHmmss) |
| stories[].data | string | Data no formato YYYY-MM-DD |
| stories[].titulo | string | Titulo curto do aprendizado |
| stories[].conteudo | string | Descricao detalhada |
| stories[].tags | string[] | Tags para busca |
| stories[].relevancia | string | alta, media ou baixa |
| metricas_resumo.total_publicados | number | Total de conteudos publicados |
| metricas_resumo.avg_retention | string | Retencao media percentual |
| metricas_resumo.avg_engagement | string | Engajamento medio percentual |
| metricas_resumo.melhor_horario | string | Horario de melhor performance |
| metricas_resumo.ultima_atualizacao | string | Data da ultima atualizacao |

---

## historico.json

Caminho: `~/conteudo/campanhas/{cliente}/historico.json`

Log cronologico de todas as publicacoes com metricas individuais.

```json
{
  "entries": [
    {
      "id": "pub_20250115180000",
      "data": "2025-01-15",
      "tipo": "post",
      "titulo": "Receita de bolo de cenoura",
      "plataformas": ["instagram", "tiktok"],
      "metricas": {
        "engajamento": "5.8%",
        "alcance": 12400,
        "retention": "72%",
        "cliques": 342
      },
      "notas": "Usou hook com legenda animada, resultado acima da media"
    }
  ]
}
```

### Campos

| Campo | Tipo | Descricao |
|-------|------|-----------|
| entries[].id | string | Identificador unico (pub_YYYYMMDDHHmmss) |
| entries[].data | string | Data de publicacao (YYYY-MM-DD) |
| entries[].tipo | string | Tipo: post, anuncio ou story |
| entries[].titulo | string | Titulo/descricao do conteudo |
| entries[].plataformas | string[] | Plataformas onde foi publicado |
| entries[].metricas.engajamento | string | Taxa de engajamento percentual |
| entries[].metricas.alcance | number | Numero de pessoas alcancadas |
| entries[].metricas.retention | string | Retencao media percentual |
| entries[].metricas.cliques | number | Total de cliques no link/CTA |
| entries[].notas | string | Observacoes livres sobre o conteudo |

### Valores validos para tipo

- `post` - Conteudo organico (feed, reels, stories)
- `anuncio` - Criativo de anuncio pago
- `story` - Story de Instagram/Facebook

---

## Validacao

Sempre valide JSON antes de salvar:

```bash
jq . ~/conteudo/campanhas/$CLIENTE/contexto.json > /dev/null
echo $?  # 0 = valido, != 0 = invalido
```
