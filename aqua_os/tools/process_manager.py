"""Process manager stub."""

from __future__ import annotations
from typing import Dict

def list_processes() -> Dict[int, str]:
    """Return a dummy process list."""
    return {1: "init"}
