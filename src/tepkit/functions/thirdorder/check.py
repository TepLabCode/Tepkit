from pathlib import Path
import logging

from tqdm import tqdm

from tepkit.core.vasp import VaspState


def is_vasp_end(path="./"):
    """
    Check if the VASP job is finished.
    """
    path = Path(path).resolve()
    outcar_path = path / "OUTCAR"
    if outcar_path.exists():
        with outcar_path.open("r") as f:
            content = f.read()
            if "Total CPU time used" in content:
                return VaspState.Finished
            else:
                return VaspState.Uncompleted
    else:
        return VaspState.Unstarted


def check_jobs(
    work_dir: str = "./",
    gap: int = 50,
    skip_info_file: Path = "tepkit.skip.info.toml",
) -> None:
    """
    Check the status of thirdorder jobs.

    :param work_dir: The path of the jobs' directory.
    :param gap: The number of jobs to display in each line.
    :param skip_info_file: The name of the skip info file.

    :typer work_dir argument:
    """

    path = Path(work_dir).resolve()
    print(path)
    job_paths = sorted(path.glob("job-*"))
    if len(job_paths) == 0:
        logging.warning("No job-* found, program exit.")
        exit()
    status = []

    for job_path in tqdm(
        job_paths,
        bar_format=R"{l_bar}{bar}| [{n_fmt:>3}/{total_fmt:>3} Jobs Checked]",
        leave=False,
    ):
        state = is_vasp_end(job_path)
        if state is VaspState.Finished:
            status.append("#")
        elif (job_path / skip_info_file).exists():
            status.append("S")
        elif state is VaspState.Uncompleted:
            status.append("R")
        else:
            status.append("_")
    status_text = "".join(status)
    status_count = {
        "finished": status.count("#") + status.count("S"),
        "unfinished": len(status_text) - status.count("#"),
        "running": status.count("R"),
        "unstarted": status.count("_"),
    }

    def progress_bar(current, maximum, bar_length=50):
        progress = int((current / maximum) * bar_length)
        precent = str(int(current / maximum * 100))
        bar = "[" + "#" * progress + "_" * (bar_length - progress) + "]"
        return f"{bar} {precent} % ({current} / {maximum})"

    def fmt(text, gap=gap):
        result = []
        last_job_num = len(text)
        for i in range(0, last_job_num, gap):
            start_index = i
            end_index = min(i + gap, last_job_num)
            line = f"{start_index + 1:03} {text[start_index:end_index]} {end_index:03}"
            result.append(line)
        return "\n".join(result)

    print("Total Progress")
    print(progress_bar(status_count["finished"], len(status_text)))
    print("Detailed Progresses")
    print(fmt(status_text))
