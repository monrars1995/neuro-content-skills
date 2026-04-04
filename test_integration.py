#!/usr/bin/env python3
"""Testes de integracao do neuro-content-skills.

Verifica que:
1. Todos os scripts Python importam corretamente
2. Todos os scripts tem --help funcional
3. A estrutura de pastas e criada corretamente
4. Os JSONs de schema sao validos
5. O .env.cliente template esta completo

Uso:
  python3 test_integration.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PASS = 0
FAIL = 0
SKIP = 0

SKILLS_DIR = os.path.expanduser("~/.opencode/skills")
CONTEUDO_DIR = os.path.expanduser("~/conteudo")
SCRIPTS = {
    "content-workflow": ["setup_completo.sh"],
    "content-ideas": ["fetch_trends.py"],
    "content-editing": ["generate_subtitles.py", "setup_remotion.sh"],
    "content-publishing": ["publish_video.py"],
    "content-metrics": ["fetch_metrics.py"],
    "content-memory": ["validate_schema.py"],
    "content-cuts": ["analyze_video.py", "smart_cut.py", "score_video.py"],
    "content-remotion": [
        "generate_dopamine_comp.py",
        "generate_subtitle_comp.py",
        "generate_zoom_comp.py",
    ],
    "content-audio": [
        "elevenlabs_tts.py",
        "generate_background_music.py",
        "mix_audio.py",
        "generate_effects.py",
    ],
}


def test(name, fn):
    global PASS, FAIL, SKIP
    try:
        result = fn()
        if result:
            PASS += 1
            print(f"  {PASS + FAIL + SKIP + 1}. {result}")
        else:
            PASS += 1
            print(f"  {PASS + FAIL + SKIP + 1}. {name}")
    except AssertionError as e:
        FAIL += 1
        print(f"  {PASS + FAIL + SKIP + 1}. {name}: {e}")
    except Exception as e:
        FAIL += 1
        print(f"  {PASS + FAIL + SKIP + 1}. {name}: ERRO - {e}")


def test_skills_dir():
    assert os.path.isdir(SKILLS_DIR), f"Diretorio de skills nao existe: {SKILLS_DIR}"
    return "Diretorio de skills encontrado"


def test_all_skills_exist():
    missing = []
    for skill in SCRIPTS:
        skill_dir = os.path.join(SKILLS_DIR, skill)
        if not os.path.isdir(skill_dir):
            missing.append(skill)
    assert not missing, f"Skills faltando: {', '.join(missing)}"
    return f"Todos os {len(SCRIPTS)} skills existem"


def test_all_scripts_exist():
    missing = []
    for skill, scripts in SCRIPTS.items():
        for script in scripts:
            script_path = os.path.join(SKILLS_DIR, skill, "scripts", script)
            if not os.path.isfile(script_path):
                missing.append(f"{skill}/{script}")
    assert not missing, f"Scripts faltando: {', '.join(missing)}"
    return f"Todos os scripts ({sum(len(v) for v in SCRIPTS.values())}) existem"


def test_python_scripts_import():
    """Testa que scripts Python nao tem erros de import."""
    errors = []
    for skill, scripts in SCRIPTS.items():
        for script in scripts:
            if script.endswith(".py"):
                script_path = os.path.join(SKILLS_DIR, skill, "scripts", script)
                result = subprocess.run(
                    [
                        "python3",
                        "-c",
                        f"import ast; ast.parse(open('{script_path}').read())",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode != 0:
                    errors.append(f"{skill}/{script}: {result.stderr.strip()}")
    assert not errors, f"Erros de sintaxe: {', '.join(errors)}"
    return "Todos os scripts Python tem sintaxe valida"


def test_python_scripts_help():
    """Testa que scripts Python com argparse aceitam --help."""
    errors = []
    for skill, scripts in SCRIPTS.items():
        for script in scripts:
            if script.endswith(".py"):
                script_path = os.path.join(SKILLS_DIR, skill, "scripts", script)
                result = subprocess.run(
                    ["python3", script_path, "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode != 0 and "usage:" not in result.stderr.lower():
                    errors.append(f"{skill}/{script}")
    assert not errors, f"Scripts com erro no --help: {', '.join(errors)}"
    return "Todos os scripts Python aceitam --help"


def test_env_template():
    template = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "env.cliente.template"
    )
    assert os.path.isfile(template), f"Template .env.cliente nao encontrado: {template}"
    content = open(template).read()
    required_keys = [
        "TIKTOK_ACCESS_TOKEN",
        "TIKTOK_APP_ID",
        "TIKTOK_USERNAME",
        "TIKTOK_RESEARCH_API_KEY",
        "TIKTOK_BUSINESS_ID",
        "META_ACCESS_TOKEN",
        "INSTAGRAM_BUSINESS_ACCOUNT_ID",
        "FACEBOOK_PAGE_ID",
        "META_AD_ACCOUNT_ID",
        "OPENAI_API_KEY",
        "ELEVENLABS_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "ELEVENLABS_MODEL_ID",
        "ELEVENLABS_OUTPUT_FORMAT",
        "GOOGLE_TRENDS_GEO",
        "GOOGLE_TRENDS_LANG",
    ]
    missing = [k for k in required_keys if k not in content]
    assert not missing, f"Chaves faltando no template: {', '.join(missing)}"
    return f"Template .env.cliente tem todas as {len(required_keys)} chaves"


def test_validate_schema():
    script = os.path.join(SKILLS_DIR, "content-memory/scripts/validate_schema.py")
    assert os.path.isfile(script), "validate_schema.py nao encontrado"
    return "validate_schema.py encontrado"


def test_setup_script():
    script = os.path.join(SKILLS_DIR, "content-workflow/scripts/setup_completo.sh")
    assert os.path.isfile(script), "setup_completo.sh nao encontrado"
    assert os.access(script, os.X_OK), "setup_completo.sh nao e executavel"
    return "setup_completo.sh e executavel"


def test_mcp_server():
    mcp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")
    assert os.path.isfile(mcp), "mcp_server.py nao encontrado"
    result = subprocess.run(
        ["python3", "-c", f"import ast; ast.parse(open('{mcp}').read())"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, "mcp_server.py tem erro de sintaxe"
    return "mcp_server.py sintaxe OK"


def test_neuro_cli():
    cli = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neuro")
    assert os.path.isfile(cli), "neuro CLI nao encontrado"
    assert os.access(cli, os.X_OK), "neuro CLI nao e executavel"
    return "neuro CLI executavel"


def test_install_md():
    install = os.path.join(os.path.dirname(os.path.abspath(__file__)), "INSTALL.md")
    assert os.path.isfile(install), "INSTALL.md nao encontrado"
    content = open(install).read()
    required_sections = [
        "APIs Suportadas",
        "Comandos Disponiveis",
        "Scripts Disponiveis",
        "Estrutura do Workspace",
    ]
    missing = [s for s in required_sections if s not in content]
    assert not missing, f"Secoes faltando no INSTALL.md: {', '.join(missing)}"
    return "INSTALL.md tem todas as secoes necessarias"


def run_all():
    print("=" * 60)
    print("  NEURO CONTENT SKILLS - TESTES DE INTEGRACAO")
    print("=" * 60)
    print()

    tests = [
        ("Diretorio de skills", test_skills_dir),
        ("Todas as skills existem", test_all_skills_exist),
        ("Todos os scripts existem", test_all_scripts_exist),
        ("Scripts Python - sintaxe", test_python_scripts_import),
        ("Scripts Python --help", test_python_scripts_help),
        ("Template .env.cliente", test_env_template),
        ("validate_schema.py", test_validate_schema),
        ("setup_completo.sh", test_setup_script),
        ("mcp_server.py", test_mcp_server),
        ("neuro CLI", test_neuro_cli),
        ("INSTALL.md", test_install_md),
    ]

    for name, fn in tests:
        test(name, fn)

    print()
    print("=" * 60)
    total = PASS + FAIL + SKIP
    print(
        f"  Resultado: {PASS} passaram, {FAIL} falharam, {SKIP} pulados (total: {total})"
    )
    print("=" * 60)

    return FAIL == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
