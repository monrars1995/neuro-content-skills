#!/usr/bin/env python3
"""Valida schemas de contexto.json e historico.json de um cliente."""

import argparse
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path.home() / "conteudo"

CONTEXT_SCHEMA = {
    "cliente": {
        "nome": str,
        "nicho": str,
        "plataformas": list,
        "tom_de_voz": str,
        "cta_padrao": str,
        "horarios_melhores": list,
    },
    "preferencias": dict,
    "stories": list,
    "metricas_resumo": dict,
}

HISTORY_SCHEMA = {
    "entries": [
        {
            "id": str,
            "data": str,
            "tipo": str,
            "titulo": str,
            "plataformas": list,
            "metricas": dict,
        }
    ]
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_TIPOS = {"post", "anuncio", "story"}
VALID_RELEVANCIA = {"alta", "media", "baixa"}


def validate_context(data: dict, path: Path) -> list:
    errors = []

    if not isinstance(data, dict):
        errors.append(f"ERRO: {path} nao e um objeto JSON valido")
        return errors

    for key in CONTEXT_SCHEMA:
        if key not in data:
            errors.append(f"AVISO: campo '{key}' ausente em {path.name}")
            continue
        val = data[key]
        expected = CONTEXT_SCHEMA[key]

        if key == "cliente":
            if not isinstance(val, dict):
                errors.append(f"ERRO: 'cliente' deve ser objeto em {path.name}")
            else:
                for field in expected:
                    if field not in val:
                        errors.append(f"AVISO: cliente.{field} ausente em {path.name}")

        elif key == "stories":
            if not isinstance(val, list):
                errors.append(f"ERRO: 'stories' deve ser array em {path.name}")
            else:
                for i, story in enumerate(val):
                    if not isinstance(story, dict):
                        errors.append(f"ERRO: stories[{i}] nao e objeto")
                        continue
                    for field in ("id", "data", "titulo", "conteudo", "tags"):
                        if field not in story:
                            errors.append(f"AVISO: stories[{i}].{field} ausente")
                    if "data" in story and not DATE_RE.match(story["data"]):
                        errors.append(
                            f"ERRO: stories[{i}].data formato invalido (use YYYY-MM-DD)"
                        )
                    if (
                        "relevancia" in story
                        and story["relevancia"] not in VALID_RELEVANCIA
                    ):
                        errors.append(
                            f"AVISO: stories[{i}].relevancia invalida: {story['relevancia']}"
                        )

        elif key == "metricas_resumo":
            if not isinstance(val, dict):
                errors.append(f"ERRO: 'metricas_resumo' deve ser objeto em {path.name}")

    return errors


def validate_history(data: dict, path: Path) -> list:
    errors = []

    if isinstance(data, list):
        errors.append(
            f"AVISO: {path.name} esta como array direto, deveria ter wrapper {{'entries': [...]}}"
        )
        entries = data
    elif isinstance(data, dict):
        if "entries" not in data:
            errors.append(f"ERRO: campo 'entries' ausente em {path.name}")
            return errors
        entries = data["entries"]
    else:
        errors.append(f"ERRO: {path.name} nao e um JSON valido")
        return errors

    if not isinstance(entries, list):
        errors.append(f"ERRO: 'entries' deve ser array em {path.name}")
        return errors

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"ERRO: entries[{i}] nao e objeto")
            continue
        for field in ("id", "data", "tipo", "titulo", "plataformas", "metricas"):
            if field not in entry:
                errors.append(f"AVISO: entries[{i}].{field} ausente")
        if "data" in entry and not DATE_RE.match(entry["data"]):
            errors.append(f"ERRO: entries[{i}].data formato invalido (use YYYY-MM-DD)")
        if "tipo" in entry and entry["tipo"] not in VALID_TIPOS:
            errors.append(f"AVISO: entries[{i}].tipo invalido: {entry['tipo']}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Valida schemas de cliente")
    parser.add_argument("--cliente", required=True, help="Nome do cliente")
    parser.add_argument(
        "--fix", action="store_true", help="Auto-corrigir problemas simples"
    )
    args = parser.parse_args()

    campaign_dir = BASE_DIR / "campanhas" / args.cliente
    if not campaign_dir.exists():
        print(f"ERRO: Diretorio do cliente nao encontrado: {campaign_dir}")
        sys.exit(1)

    all_errors = []

    context_path = campaign_dir / "contexto.json"
    if context_path.exists():
        data = json.loads(context_path.read_text())
        errors = validate_context(data, context_path)
        all_errors.extend(errors)
        if not errors:
            print(f"OK: {context_path.name} - schema valido")
    else:
        print(f"AVISO: {context_path.name} nao encontrado")

    history_path = campaign_dir / "historico.json"
    if history_path.exists():
        data = json.loads(history_path.read_text())
        errors = validate_history(data, history_path)
        all_errors.extend(errors)

        if args.fix and isinstance(data, list):
            wrapped = {"entries": data}
            history_path.write_text(json.dumps(wrapped, indent=2, ensure_ascii=False))
            print(
                f"CORRIGIDO: {history_path.name} - array envelopado em {{'entries': [...]}}"
            )
        elif not errors:
            print(f"OK: {history_path.name} - schema valido")
    else:
        print(f"AVISO: {history_path.name} nao encontrado")

    if all_errors:
        print(f"\n{len(all_errors)} problema(s) encontrado(s):")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\nTodos os schemas estao validos!")


if __name__ == "__main__":
    main()
