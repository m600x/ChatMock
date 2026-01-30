from __future__ import annotations

from flask import current_app
import os
import sys
from pathlib import Path


CLIENT_ID_DEFAULT = os.getenv("CHATGPT_LOCAL_CLIENT_ID") or "app_EMoamEEZ73f0CkXaXp7hrann"
OAUTH_ISSUER_DEFAULT = os.getenv("CHATGPT_LOCAL_ISSUER") or "https://auth.openai.com"
OAUTH_TOKEN_URL = f"{OAUTH_ISSUER_DEFAULT}/oauth/token"
verbose = bool(current_app.config.get("VERBOSE"))

CHATGPT_RESPONSES_URL = "https://chatgpt.com/backend-api/codex/responses"


def _read_prompt_text(filename: str) -> str | None:
    candidates = [
        Path(__file__).parent.parent / filename,
        Path(__file__).parent / filename,
        Path(getattr(sys, "_MEIPASS", "")) / filename if getattr(sys, "_MEIPASS", None) else None,
        Path.cwd() / filename,
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            if candidate.exists():
                content = candidate.read_text(encoding="utf-8")
                if isinstance(content, str) and content.strip():
                    return content
        except Exception:
            continue
    return None


def read_base_instructions() -> str:
    filepath = os.getenv("PROMPT_PATH") or "prompt.md"
    if verbose:
        print(f"Reading base prompt from: {filepath}")
    content = _read_prompt_text(filepath)
    if content is None:
        raise FileNotFoundError(f"Failed to read {filepath}; expected adjacent to package or CWD.")
    return content


def read_gpt5_codex_instructions(fallback: str) -> str:
    filepath = os.getenv("PROMPT_GPT5_CODEX_PATH") or "prompt_gpt5_codex.md"
    if verbose:
        print(f"Reading GPT-5 Codex prompt from: {filepath}")
    content = _read_prompt_text(filepath)
    if content is None or content.strip() == "":
        return fallback
    return content


BASE_INSTRUCTIONS = read_base_instructions()
GPT5_CODEX_INSTRUCTIONS = read_gpt5_codex_instructions(BASE_INSTRUCTIONS)
