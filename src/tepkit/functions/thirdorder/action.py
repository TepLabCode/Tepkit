import os
import shutil
from pathlib import Path

import toml


def _set_jobs(
    work_dir: Path,
    incar: Path = "./INCAR",
    kpoints: Path = "./KPOINTS",
    potcar: Path = "./POTCAR",
    pattern: str = "*.POSCAR.*",
):
    # Check input files / 检查输入文件
    for file in [incar, kpoints, potcar]:
        file = Path(file).resolve()
        if not file.exists():
            raise FileNotFoundError(f"Can not found file at {str(file)}.")
    # Glob `*.POSCAR.*` files / 匹配 `*.POSCAR.*` 文件列表
    poscars = list(Path(".").glob(pattern))
    if len(poscars) == 0:
        raise FileNotFoundError(f"Can not found any file match pattern {pattern}.")
    # Create work_dir / 创建工作目录
    work_dir = Path(work_dir).resolve()
    os.makedirs(work_dir, exist_ok=True)
    # Remove old job-* directories / 删除旧的 job-* 目录
    for job_dir in work_dir.glob("job-*"):
        shutil.rmtree(job_dir, ignore_errors=True)
    # Copy input files to work_dir / 复制输入文件到工作目录
    shutil.copy(incar, work_dir / "INCAR")
    shutil.copy(kpoints, work_dir / "KPOINTS")
    shutil.copy(potcar, work_dir / "POTCAR")
    # Process each `*.POSCAR.*` file / 处理每个 `*.POSCAR.*` 文件
    for poscar in poscars:
        job_id = poscar.name.split(".")[-1]
        job_dir = work_dir / f"job-{job_id}"
        job_dir.mkdir()
        # Move `*.POSCAR.<id>` to `job-<id>/POSCAR`
        poscar.rename(job_dir / "POSCAR")
        # Link `INCAR & KPOINTS & POTCAR` to `job-<id>/*`
        for file in ["INCAR", "KPOINTS", "POTCAR"]:
            (job_dir / file).symlink_to(work_dir / file)
    logger.done(f"All {len(poscars)} jobs set up successfully!")


def set_jobs_3rd(
    work_dir: Path,
    incar: Path = "./INCAR",
    kpoints: Path = "./KPOINTS",
    potcar: Path = "./POTCAR",
):
    """
    Set the job folders.

    :typer work_dir flag: --to
    :typer incar panel: Required Files
    :typer kpoints panel: Required Files
    :typer potcar panel: Required Files
    """
    return _set_jobs(work_dir, incar, kpoints, potcar, "3RD.POSCAR.*")


def set_jobs_4th(
    work_dir: Path,
    incar: Path = "./INCAR",
    kpoints: Path = "./KPOINTS",
    potcar: Path = "./POTCAR",
):
    """
    Set the job folders.

    :typer work_dir flag: --to
    :typer incar panel: Required Files
    :typer kpoints panel: Required Files
    :typer potcar panel: Required Files
    """
    return _set_jobs(work_dir, incar, kpoints, potcar, "4TH.POSCAR.*")


def read_header(file_path):
    with open(file_path, "r") as f:
        return f.readline().strip()


from tepkit.cli import logger


def _file_action(action: str, from_file: Path, to_file: Path):
    if action in ["none", "write"]:
        return
    if to_file.is_symlink():
        to_file.unlink()
        logger.info("Link found, unlinked it.")
    elif to_file.is_file():
        bak_path = to_file.with_name(to_file.name + ".bak")
        if bak_path.exists():
            bak_path.unlink()
        to_file.rename(bak_path)
        logger.c.info(
            f"<lk>File `{from_file.name}` found, renamed it to `{bak_path.name}`.</>"
        )
    match action:
        case "link":
            to_file.symlink_to(from_file)
            logger.info("Link created.")
        case "copy":
            shutil.copy(from_file, to_file)
        case _:
            raise ValueError(f"Invalid action: {action}")


def adjust_cutoff(
    old_work_dir: Path,
    new_work_dir: Path,
    action: str = "copy",  # none | write | link | copy
):
    """
    Adjust the cutoff radius of the 3rd order force constants.

    :param old_work_dir: The work directory containing completed jobs.
    :param new_work_dir: The work directory containing the jobs with new cutoff radius.
    :param action: The action to take for the duplicate jobs.
                   - none: Only print the duplicate jobs. &
                   - write: Write the skip info file to the directory of the duplicate job. &
                   - link: `write` + also create a symbolic link to the vasprun.xml of the old job. &
                   - copy: `write` + also copy the vasprun.xml of the old job to new jobs.
    :typer old_work_dir flag: --old-dir, --old
    :typer new_work_dir flag: --new-dir, --new
    """

    old_work_dir = Path(old_work_dir).resolve()
    new_work_dir = Path(new_work_dir).resolve()

    old_jobs = sorted([job for job in list(old_work_dir.glob("job-*")) if job.is_dir()])
    new_jobs = sorted([job for job in list(new_work_dir.glob("job-*")) if job.is_dir()])
    old_headers = [read_header(job / "POSCAR") for job in old_jobs]
    new_headers = [read_header(job / "POSCAR") for job in new_jobs]
    action_files = ["vasprun.xml"]

    for new_job, new_header in zip(new_jobs, new_headers):
        if new_header in old_headers:
            old_job = old_jobs[old_headers.index(new_header)]
            logger.info(f"[new] {new_job.name} = [old] {old_job.name}")
            if action in ["write", "link", "copy"]:
                with open(new_job / "tepkit.skip.info.toml", "w") as file:
                    file.write(
                        f'"{new_job.name}" = "{old_job.name} ({old_work_dir.name})"'
                    )
            for file in action_files:
                _file_action(action, old_job / file, new_job / file)


def check_duplicate_jobs(
    work_dir: Path = "./",
    action: str = "write",  # none | write | link | copy
    skip_info_file: Path = "tepkit.skip.info.toml",
    info_file: Path = "tepkit.check_duplicate_jobs.info.toml",
    fast: bool = False,
):
    """
    Find duplicate jobs.

    :param work_dir: The work directory containing the job-* folders.
    :param action: The action to take for the duplicate jobs.
                   - none: Only print the duplicate jobs. &
                   - write: Write the skip info file to the directory of the duplicate job. &
                   - link: `write` + also create a symbolic link to the vasprun.xml of the first matched job. &
                   - copy: `write` + also copy the vasprun.xml of the first matched job to the other jobs.
    :param skip_info_file: The file save to the directory of the duplicate job.
    :param info_file: The file to save the duplicate job info.
    :param fast: If True, only check the hash header of the POSCAR file.

    :typer work_dir flag: --dir, --work-dir
    """
    work_path = Path(work_dir).resolve()
    jobs = sorted([job for job in list(work_path.glob("job-*")) if job.is_dir()])
    if len(jobs) == 0:
        logger.error(f"No job found in the path `{work_path}`.")
        logger.info("Please use `--dir` to specify the correct work directory.")
        return
    logger.done(f"Found {len(jobs)} jobs, start checking.")
    headers = [read_header(job / "POSCAR") for job in jobs]
    action_files = ["vasprun.xml"]
    strict_check = not fast
    results = {}

    for job, header in zip(jobs, headers):
        first_job = jobs[headers.index(header)]
        if job != first_job:
            if strict_check:
                path1 = job / "POSCAR"
                path2 = first_job / "POSCAR"
                with open(path1, "r") as file1, open(path2, "r") as file2:
                    content1 = file1.read()
                    content2 = file2.read()
                    if content1 != content2:
                        logger.warning(
                            f"{job.name} and {first_job.name} have same hash but different content!"
                        )
                        continue
            logger.info(f"{job.name} = {first_job.name}")
            results[job.name] = first_job.name
            if action in ["write", "link", "copy"]:
                with open(job / skip_info_file, "w") as file:
                    file.write(f'"{job.name}" = "{first_job.name}"')
            for file in action_files:
                _file_action(action, first_job / file, job / file)
    logger.done(f"Found {len(results)} duplicate jobs in total {len(jobs)} jobs.")
    with open(info_file, "w") as file:
        toml.dump(results, file)
    logger.success(f"Duplicate job info saved to `{info_file}`.")
