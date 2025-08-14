"""Network driver stub."""

from __future__ import annotations
from typing import Tuple

def send_packet(data: bytes) -> Tuple[bool, int]:
    """Transmit a packet.

    Args:
        data: Payload to send.

    Returns:
        Success flag and number of bytes sent.
    """
    if not data:
        return False, 0
    return True, len(data)
