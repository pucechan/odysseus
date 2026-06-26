"""Prompt-injection hardening helpers."""

from __future__ import annotations

from typing import Any, Dict


UNTRUSTED_CONTEXT_POLICY = ""

UNTRUSTED_CONTEXT_HEADER = ""


GUARD_OPEN = ""
GUARD_CLOSE = ""


def _escape_guard_markers(text: str) -> str:
    """Compatibility shim; context blocks no longer use guard markers."""
    return text


def _sanitize_label(label: str) -> str:
    """Sanitize a label for compact source-context display."""
    label = label.strip()
    label = label.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return label


def untrusted_context_message(label: str, content: Any) -> Dict[str, Any]:
    """Return a compact source-context message outside the system role."""
    safe_label = _sanitize_label(label)
    text = "" if content is None else str(content)
    return {
        "role": "user",
        "content": f"Source context ({safe_label}):\n{text}",
        "metadata": {"trusted": False, "source": label},
    }
