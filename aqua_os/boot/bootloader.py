"""Boot loader module compliant with DO-178C Level A.
Implements deterministic checksum verification per ARINC 653 partition loader.
"""

from __future__ import annotations
import binascii
from pathlib import Path

def calculate_checksum(image_path: Path) -> int:
    """Compute CRC32 of the image file.

    Args:
        image_path: Path to the image.

    Returns:
        32-bit CRC.

    Raises:
        FileNotFoundError: if ``image_path`` does not exist.
        ValueError: if ``image_path`` is not readable.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"{image_path} not found")
    try:
        data = image_path.read_bytes()
    except OSError as exc:  # pragma: no cover - hardware-specific error
        raise ValueError(f"Unable to read image: {exc}") from exc
    return binascii.crc32(data) & 0xFFFFFFFF
