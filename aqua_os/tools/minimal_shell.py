"""Minimal user-space shell."""

from __future__ import annotations

def run_command(cmd: str) -> str:
    """Execute a command in the mock shell."""
    return f"executed {cmd}"
