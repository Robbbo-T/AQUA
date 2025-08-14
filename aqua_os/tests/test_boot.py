from pathlib import Path
from aqua_os.boot.bootloader import calculate_checksum


def test_calculate_checksum(tmp_path: Path) -> None:
    image = tmp_path / "kernel.img"
    image.write_bytes(b"AQUA")
    assert calculate_checksum(image) == 0xA9857CD4
