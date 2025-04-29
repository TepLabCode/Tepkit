from pathlib import Path

from tepkit.cli import logger
from tepkit.utils.rich_tools import print_panel


def stop_vasp(
    ele: bool = False,
    ion: bool = False,
    job_dir: Path = "./",
):
    """
    Stop the VASP process by STOPCAR.

    Use (-e / -i / -ei) to generate STOPCAR file.

    :param ele    : VASP will stop at the next electronic step.
    :param ion    : VASP will stop at the next ionic step.
    :param job_dir: the path of the VASP's jobdir.

    :typer ele     flag: --ele, -e
    :typer ion     flag: --ion, -i
    :typer job_dir flag: --dir
    """
    content_lines = [
        "# Stop at the next electronic step",
        "LABORT = .TRUE." if ele else "# LABORT = .TRUE.",
        "",
        "# Stop at the next ionic step",
        "LSTOP  = .TRUE." if ion else "# LSTOP  = .TRUE.",
        "",
    ]
    content = "\n".join(content_lines)
    save_path = Path(job_dir).resolve() / "STOPCAR"
    logger.info("The STOPCAR file is generated as below:")
    print_panel(content, title="STOPCAR")
    with open(save_path, "w") as file:
        file.write(content)
    logger.done(f"The STOPCAR file is saved to {save_path}.")


def clear_outputs(
    job_dir: Path = "./",
    and_files: list[Path] = None,
    keep_files: list[Path] = None,
    backup_files: list[Path] = None,
):
    """
    Clear the VASP's output files.

    :param job_dir: the path of the VASP's jobdir.
    :param and_files: the files will be removed together with the VASP output files.
    :param keep_files: the files will be kept and not removed.
    :param backup_files: the files will be backuped to `*.bak` before removing.

    :typer job_dir flag: --dir
    :typer and_files flag: --and, --also
    :typer keep_files flag: --keep, --skip
    :typer backup_files flag: --backup, --bak
    """
    output_files = [
        "CHG", "CHGCAR", "CONTCAR", "STOPCAR",
        "DOSCAR", "DYNMAT", "EIGENVAL", "IBZKPT",
        "OPTIC", "OSZICAR", "OUTCAR", "PROCAR",
        "PCDAT", "WAVECAR", "XDATCAR", "PARCHG",
        "REPORT", "PENALTYPOT", "HILLSPOT",
        "wannier90.win", "wannier90_band.gnu", "wannier90_band.kpt",
        "wannier90.chk", "wannier90.wout",
        "vasprun.xml", "vaspout.h5",
        "ML_LOGFILE", "ML_ABN", "ML_FFN", "ML_HIS", "ML_REG",
    ]  # fmt: skip
    job_dir = Path(job_dir).resolve()
    output_files = [job_dir / file for file in output_files]
    and_files = [job_dir / file for file in and_files] if and_files else []
    keep_files = [job_dir / file for file in keep_files] if keep_files else []
    backup_files = [job_dir / file for file in backup_files] if backup_files else []  # fmt: skip

    for file in output_files + and_files:
        if file.exists():
            if file in keep_files:
                logger.c.info(f"File <cyan>{file.name}</> is <green>kept</>, skip.")
                continue
            elif file in backup_files:
                backup_path = file.parent / f"{file.name}.bak"
                if backup_path.exists():
                    backup_path.unlink()
                file.rename(backup_path)
                logger.c.info(f"File <cyan>{file.name}</> is <blue>backuped</> to <cyan>{backup_path.name}</>.")  # fmt: skip
            else:
                file.unlink()
                logger.c.info(f"File <cyan>{file.name}</> is <yellow>removed</>.")
        else:
            logger.c.trace(f"<light-black>File {file.name} does not exist, skip.</>")
