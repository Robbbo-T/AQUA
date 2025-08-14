"""Deterministic task scheduler for MOS kernel (ARINC 653 partition)."""

from __future__ import annotations
from typing import List

def round_robin(tasks: List[str]) -> List[str]:
    """Rotate task list by one position.

    Args:
        tasks: Ordered list of task identifiers.

    Returns:
        Rotated task list.
    """
    if not tasks:
        return []
    return tasks[1:] + tasks[:1]
