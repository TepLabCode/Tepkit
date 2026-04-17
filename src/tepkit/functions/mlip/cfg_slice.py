from pathlib import Path


def cfg_slice_cli(
    path: Path,
    start: int = None,
    end: int = None,
    step: int = None,
    output: str = None,
    rest: str = None,
):
    """
    Slice a MLIP cfg file.

    :typer path argument:
    """
    print(locals())
    pass
