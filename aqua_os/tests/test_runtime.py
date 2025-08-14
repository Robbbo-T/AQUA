from aqua_os.runtime.startup import initialize_runtime


def test_initialize_runtime() -> None:
    assert initialize_runtime() is True
