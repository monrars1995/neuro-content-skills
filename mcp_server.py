#!/usr/bin/env python3
"""
Neuro Content Skills - MCP Server
Expoe todas as 13 skills como ferramentas para agentes de IA.

Instalacao:
  pip3 install mcp

Uso no Claude Desktop (claude_desktop_config.json):
  {
    "mcpServers": {
      "neuro-content": {
        "command": "python3",
        "args": ["/caminho/para/neuro-content-skills/mcp_server.py"]
      }
    }
  }

Uso com OpenCode / outros clientes MCP:
  python3 mcp_server.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

CONTEUDO_DIR = os.path.expanduser("~/conteudo")
SKILLS_DIR = os.path.expanduser("~/.opencode/skills")

TOOLS = [
    {
        "name": "neuro_status",
        "description": "Painel de status de todos os clientes. Lista clientes, conteudo em cada fase e metricas.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "neuro_criar_cliente",
        "description": "Cria um novo cliente com toda a estrutura de pastas, contexto.json, historico.json e .env.cliente.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nome": {"type": "string", "description": "Slug do cliente (ex: joao-academia)"},
                "nicho": {"type": "string", "description": "Nicho/segmento (ex: fitness, financas)"},
                "plataformas": {"type": "array", "items": {"type": "string"}, "description": "Lista de plataformas (tiktok, instagram, youtube)"},
                "tom_de_voz": {"type": "string", "description": "Tom de voz (educativo, humor, inspiracional)"},
            },
            "required": ["nome", "nicho"],
        },
    },
    {
        "name": "neuro_contexto",
        "description": "Consulta a memoria/contexto de um cliente (contexto.json). Retorna preferencias, stories e metricas resumo.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
            },
            "required": ["cliente"],
        },
    },
    {
        "name": "neuro_historico",
        "description": "Consulta o historico de publicacoes de um cliente (historico.json). Retorna todas as entradas com metricas.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
            },
            "required": ["cliente"],
        },
    },
    {
        "name": "neuro_listar_midias",
        "description": "Lista arquivos de midia de um cliente em uma fase especifica. Suporta ideias, roteiros, brutos, editados, publicados.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "tipo": {"type": "string", "description": "Tipo de conteudo (posts-midias-sociais ou criativos-anuncios)"},
                "fase": {"type": "string", "description": "Fase (ideias, roteiros, brutos, editados, publicados)"},
            },
            "required": ["cliente", "tipo", "fase"],
        },
    },
    {
        "name": "neuro_analisar_video",
        "description": "Analisa um video completo para identificar pontos de corte otimos. Detecta silencios, mudancas de cena e trechos com alta densidade de fala.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "video": {"type": "string", "description": "Caminho do video"},
            },
            "required": ["cliente", "video"],
        },
    },
    {
        "name": "neuro_gerar_cortes",
        "description": "Gera cortes virais otimizados para short-form a partir de um video analise. Suporta reels, shorts e tiktok.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "video": {"type": "string", "description": "Caminho do video"},
                "plataforma": {"type": "string", "enum": ["reels", "shorts", "tiktok"], "description": "Plataforma destino"},
                "max_duracao": {"type": "number", "description": "Duracao maxima em segundos (padrao: 90)"},
            },
            "required": ["cliente", "video"],
        },
    },
    {
        "name": "nero_pontuar_video",
        "description": "Avalia o potencial viral de um video com rubrica detalhada (0-100). Avalia hook, ritmo, engajamento, formato, audio e CTA.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "video": {"type": "string", "description": "Caminho do video"},
            },
            "required": ["cliente", "video"],
        },
    },
    {
        "name": "neuro_legendas",
        "description": "Gera legendas automaticas para um video usando Whisper (local ou OpenAI API). Suporta saidas SRT, JSON e Remotion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "video": {"type": "string", "description": "Caminho do video"},
                "formato": {"type": "string", "enum": ["srt", "json", "remotion", "todos"], "description": "Formato de saida (padrao: todos)"},
            },
            "required": ["cliente", "video"],
        },
    },
    {
        "name": "neuro_voz",
        "description": "Gera voz AI (TTS) a partir de texto usando ElevenLabs. Suporta texto direto ou arquivo de roteiro.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
                "texto": {"type": "string", "description": "Texto para gerar voz"},
                "arquivo": {"type": "string", "description": "Caminho do arquivo de texto"},
                "voz_id": {"type": "string", "description": "ID da voz ElevenLabs (padrao: do .env.cliente)"},
            },
            "required": ["cliente"],
        },
    },
    {
        "name": "neuro_musicas",
        "description": "Lista vozes disponiveis na conta ElevenLabs. Filtra por idioma.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "idioma": {"type": "string", "description": "Filtrar por idioma (ex: pt, en, es)"},
            },
        },
    },
    },
    {
        "name": "neuro_trends",
        "description": "Pesquisa trends atuais do nicho do cliente via TikTok Research API e Google Trends.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nome do cliente"},
            },
            "required": ["cliente"],
        },
    },
]


def load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def run_script(script_path: str, args: list) -> str:
    try:
        result = subprocess.run(
            ["python3", script_path] + args,
            capture_output=True, text=True, timeout=120,
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            return f"ERRO: {result.stderr.strip()}"
        return output if output else "(sem saida)"
    except FileNotFoundError:
        return f"ERRO: Script nao encontrado: {script_path}"
    except subprocess.TimeoutExpired:
        return "ERRO: Timeout (120s)"
    except Exception as e:
        return f"ERRO: {e}"


def get_client_dir(cliente: str) -> str:
    return os.path.join(CONTEUDO_DIR, "campanhas", cliente)


def handle_neuro_status(args: dict) -> str:
    result = []
    campanhas = os.path.join(CONTEUDO_DIR, "campanhas")
    if not os.path.isdir(campanhas):
        return "Nenhum cliente encontrado. Use neuro_criar_cliente primeiro."
    for d in sorted(os.listdir(campanhas)):
        client_path = os.path.join(campanhas, d)
        if not os.path.isdir(client_path):
            continue
        ctx = load_json(os.path.join(client_path, "contexto.json"))
        nicho = ctx.get("cliente", {}).get("nicho", "?")
        plataformas = ctx.get("cliente", {}).get("plataformas", [])
        total_pub = ctx.get("metricas_resumo", {}).get("total_publicados", 0)
        items = []
        for tipo in ["posts-midias-sociais", "criativos-anuncios"]:
            for fase in ["ideias", "roteiros", "brutos", "editados", "publicados"]:
                fase_dir = os.path.join(client_path, tipo, fase)
                if os.path.isdir(fase_dir):
                    count = len([f for f in os.listdir(fase_dir) if not f.startswith(".")])
                    if count > 0:
                        items.append(f"{fase}: {count}")
        result.append(f"{d} ({nicho}) | Plataformas: {', '.join(plataformas) if plataformas else 'nenhuma'} | Publicados: {total_pub}")
        if items:
            result.append("  " + " | ".join(items))
    return "\n".join(result) if result else "Nenhum cliente encontrado."


def handle_neuro_criar_cliente(args: dict) -> str:
    nome = args["nome"].lower().replace(" ", "-")
    nicho = args.get("nicho", "")
    plataformas = args.get("plataformas", [])
    tom = args.get("tom_de_voz", "")
    base = get_client_dir(nome)
    os.makedirs(base, exist_ok=True)
    for tipo in ["posts-midias-sociais", "criativos-anuncios"]:
        for fase in ["ideias", "roteiros", "brutos", "editados", "publicados"]:
            os.makedirs(os.path.join(base, tipo, fase), exist_ok=True)
    os.makedirs(os.path.join(base, "briefings"), exist_ok=True)
    os.makedirs(os.path.join(base, "metricas"), exist_ok=True)
    ctx = {
        "cliente": {"nome": nome, "nicho": nicho, "plataformas": plataformas, "tom_de_voz": tom, "cta_padrao": "", "horarios_melhores": []},
        "preferencias": {},
        "stories": [],
        "metricas_resumo": {"total_publicados": 0, "avg_retention": "0%", "avg_engagement": "0%", "melhor_horario": "", "ultima_atualizacao": ""},
    }
    with open(os.path.join(base, "contexto.json"), "w", encoding="utf-8") as f:
        json.dump(ctx, f, indent=2, ensure_ascii=False)
    with open(os.path.join(base, "historico.json"), "w", encoding="utf-8") as f:
        json.dump({"entries": []}, f, indent=2)
    open(os.path.join(base, ".env.cliente"), "a").close()
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "env.cliente.template")
    if os.path.exists(template):
        with open(template) as src, open(os.path.join(base, ".env.cliente"), "w") as dst:
            dst.write(src.read())
    return f"Cliente '{nome}' criado em {base}"


def handle_neuro_contexto(args: dict) -> str:
    path = os.path.join(get_client_dir(args["cliente"]), "contexto.json")
    return json.dumps(load_json(path), indent=2, ensure_ascii=False)


def handle_neuro_historico(args: dict) -> str:
    path = os.path.join(get_client_dir(args["cliente"]), "historico.json")
    return json.dumps(load_json(path), indent=2, ensure_ascii=False)


def handle_neuro_listar_midias(args: dict) -> str:
    dir_path = os.path.join(get_client_dir(args["cliente"]), args["tipo"], args["fase"])
    if not os.path.isdir(dir_path):
        return f"Diretorio nao encontrado: {dir_path}"
    files = [f for f in os.listdir(dir_path) if not f.startswith(".")]
    if not files:
        return "Nenhum arquivo encontrado."
    return "\n".join(files)


def handle_neuro_analisar_video(args: dict) -> str:
    return run_script(
        os.path.join(SKILLS_DIR, "content-cuts/scripts/analyze_video.py"),
        ["--video", args["video"], "--cliente", args["cliente"]],
    )


def handle_neuro_gerar_cortes(args: dict) -> str:
    cmd_args = ["--video", args["video"], "--cliente", args["cliente"]]
    if "plataforma" in args:
        cmd_args += ["--plataforma", args["plataforma"]]
    if "max_duracao" in args:
        cmd_args += ["--max-duracao", str(args["max_duracao"])]
    return run_script(
        os.path.join(SKILLS_DIR, "content-cuts/scripts/smart_cut.py"), cmd_args
    )


def handle_neuro_pontuar_video(args: dict) -> str:
    return run_script(
        os.path.join(SKILLS_DIR, "content-cuts/scripts/score_video.py"),
        ["--video", args["video"], "--cliente", args["cliente"]],
    )


def handle_neuro_legendas(args: dict) -> str:
    cmd_args = ["--video", args["video"], "--cliente", args["cliente"]]
    if "formato" in args:
        cmd_args += ["--formato", args["formato"]]
    return run_script(
        os.path.join(SKILLS_DIR, "content-editing/scripts/generate_subtitles.py"), cmd_args
    )


def handle_neuro_voz(args: dict) -> str:
    cmd_args = ["--cliente", args["cliente"]]
    if "texto" in args:
        cmd_args += ["--texto", args["texto"]]
    if "arquivo" in args:
        cmd_args += ["--arquivo", args["arquivo"]]
    if "voz_id" in args:
        cmd_args += ["--voz", args["voz_id"]]
    return run_script(
        os.path.join(SKILLS_DIR, "content-audio/scripts/elevenlabs_tts.py"), cmd_args
    )


def handle_neuro_musicas(args: dict) -> str:
    cmd_args = ["--listar-vozes"]
    if "idioma" in args:
        cmd_args += ["--idioma", args["idioma"]]
    return run_script(
        os.path.join(SKILLS_DIR, "content-audio/scripts/elevenlabs_tts.py"), cmd_args
    )


def handle_neuro_trends(args: dict) -> str:
    ctx = load_json(os.path.join(get_client_dir(args["cliente"]), "contexto.json"))
    nicho = ctx.get("cliente", {}).get("nicho", "")
    return run_script(
        os.path.join(SKILLS_DIR, "content-ideas/scripts/fetch_trends.py"),
        ["--nicho", nicho, "--cliente", args["cliente"]],
    )


HANDLERS = {
    "neuro_status": handle_neuro_status,
    "neuro_criar_cliente": handle_neuro_criar_cliente,
    "neuro_contexto": handle_neuro_contexto,
    "neuro_historico": handle_neuro_historico,
    "neuro_listar_midias": handle_neuro_listar_midias,
    "neuro_analisar_video": handle_neuro_analisar_video,
    "neuro_gerar_cortes": handle_neuro_gerar_cortes,
    "neuro_pontuar_video": handle_neuro_pontuar_video,
    "neuro_legendas": handle_neuro_legendas,
    "neuro_voz": handle_neuro_voz,
    "neuro_musicas": handle_neuro_musicas,
    "neuro_trends": handle_neuro_trends,
}


def main():
    for line in sys.stdin:
        req = json.loads(line)
        method = req.get("method")
        tool_name = req.get("name", "")
        params = req.get("arguments", {})

        if method == "tools/list":
            print(json.dumps({"tools": TOOLS}))
        elif method == "tools/call":
            handler = HANDLERS.get(tool_name)
            if handler:
                result = handler(params)
                print(json.dumps({"content": [{"type": "text", "text": result}]}))
            else:
                print(json.dumps({"content": [{"type": "text", "text": f"Ferramenta desconhecida: {tool_name}"}]}))
                print(json.dumps({"isError": True}))
        else:
            print(json.dumps({"error": f"Metodo nao suportado: {method}"}))
            print(json.dumps({"isError": True}))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
