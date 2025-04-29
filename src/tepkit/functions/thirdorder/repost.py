import os
import shutil
from pathlib import Path
from subprocess import run

from tepkit.cli import logger
from tepkit.config import get_config


def prase_path(path_str: str) -> Path:
    if "%LocalAppData%" in path_str:
        path_str = path_str.replace("%LocalAppData%", os.getenv("LocalAppData") or "")
    return Path(path_str)


def _process_command_result(result):
    # Normal Output
    print(result.stdout)
    # Error Handling
    stderr = result.stderr
    if stderr:
        print(stderr)
        if ("ModuleNotFoundError" in stderr) and ("thirdorder_core" in stderr):
            raise ModuleNotFoundError(
                "`thirdorder_core` is not properly installed.\n"
                "You can retry after you have installed thirdorder_core properly."
            )
        elif ("ImportError" in stderr) and ("symspg" in stderr):
            raise ImportError(
                "thirdorder can not find the `symspg.dll` or `libsymspg.so.2` file.\n"
                "You need to add the dir of the library file to your environment first."
            )
    #


def _vasp_sow(args: tuple[int, int, int, str], name: str):
    config = get_config()
    thirdorder_vasp_path = prase_path(config[name][f"{name}_vasp_path"])
    python_command = Path(config["python"]["python_command"])
    if not thirdorder_vasp_path.exists():
        raise FileNotFoundError(
            f"Can not found {name}_vasp.py at {thirdorder_vasp_path}."
        )
    if not Path("POSCAR").exists():
        raise FileNotFoundError("Can not found POSCAR in current directory.")
    command = f"{python_command} {thirdorder_vasp_path} sow {args[0]} {args[1]} {args[2]} {args[3]}"
    result = run(command, shell=True, text=True, capture_output=True)
    _process_command_result(result)


def vasp_sow_3rd(args: tuple[int, int, int, str]):
    """
    Run ``python thirdorder_vasp.py sow na nb nc cutoff`` command.

    Examples:
    >>> tepkit thirdorder vasp_sow -a 5 5 1 -2
    >>> tepkit thirdorder vasp_sow --args 4 4 4 6.3

    Required files:
    | POSCAR
    Output files:
    | 3RD.SPOSCAR
    | 3RD.POSCAR.*

    :typer args flag: -a, --args
    :typer args metavar: na nb nc cutoff
    """
    return _vasp_sow(args, "thirdorder")


def vasp_sow_4th(args: tuple[int, int, int, str]):
    """
    Run ``python Fourthorder_vasp.py sow na nb nc cutoff`` command.

    Examples:
    >>> tepkit fourthorder vasp_sow -a 5 5 1 -2
    >>> tepkit fourthorder vasp_sow --args 4 4 4 6.3

    Required files:
    | POSCAR
    Output files:
    | 4TH.SPOSCAR
    | 4TH.POSCAR.*

    :typer args flag: -a, --args
    :typer args metavar: na nb nc cutoff
    """
    return _vasp_sow(args, "fourthorder")


def vasp_reap(
    args: tuple[int, int, int, str],
    work_dir: Path,
    poscar: Path = "./POSCAR",
    to: Path = "./FORCE_CONSTANTS_3RD",
):
    """
    run the thirdorder_vasp.py reap.

    :param args: The arguments of reap command.
    :param poscar:  The path of POSCAR file.
    :param work_dir: The directory contains job-* folders.
    :param to: The path to save the FORCE_CONSTANTS_3RD file.
    :typer args metavar: na nb nc cutoff
    :typer args flag: -a, --args
    :typer work_dir flag: --from
    :typer poscar panel: Required Files
    :typer to     panel: Output Files
    """
    if not Path(poscar).exists():
        raise FileNotFoundError(f"Can not found POSCAR at {poscar}.")

    temp_dir = Path("tepkit_vasp_reap_temp_dir")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    shutil.copy(poscar, temp_dir / "POSCAR")

    config = get_config()
    thirdorder_vasp_path = prase_path(config["thirdorder"]["thirdorder_vasp_path"])
    python_command = Path(config["python"]["python_command"])
    if not thirdorder_vasp_path.exists():
        raise FileNotFoundError(
            f"Can not found `thirdoorder_vasp.py` at `{thirdorder_vasp_path}`.\n"
            "You need to fill the correct `thirdorder_vasp_path` in `tepkit.custom.config.toml`."
        )

    files = sorted(Path(work_dir).glob("job-*/vasprun.xml"))
    files_str = "\n".join(str(file.resolve()) for file in files)
    commands = [python_command, thirdorder_vasp_path, "reap", *[str(i) for i in args]]
    result = run(
        commands,
        input=files_str,
        text=True,
        cwd=temp_dir,
        capture_output=True,
    )
    _process_command_result(result)
    if to.exists():
        logger.warning(f"File {to} already exists, it will be overwritten.")
    shutil.copy(temp_dir / "FORCE_CONSTANTS_3RD", to)
    shutil.rmtree(temp_dir)
