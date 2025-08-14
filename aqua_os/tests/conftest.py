"""PyTest configuration for AQUA OS tests.

Ensures the project root directory is on ``sys.path`` so that ``aqua_os``
package modules can be imported without requiring ``PYTHONPATH`` environment
variables. This mimics installation behavior and simplifies local test runs.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path for module resolution.
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
