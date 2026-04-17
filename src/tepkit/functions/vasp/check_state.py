"""
``tepkit vasp check <path>``
``tepkit vasp check-dirs --root <path> --pattern <pattern>``
"""

from pathlib import Path

from tepkit.cli import logger
from tepkit.core.vasp import VaspState, check_vasp_dir_state


def check_vasp_dir_state_cli(path: Path = ".") -> None:
    """
    Check the state of a VASP job.

    :param path: The path of the job's directory.

    :typer path argument:
    """
    path = Path(path).resolve()
    logger.raw.info(f"Path: {path}\n")
    if not path.exists():
        logger.error(f"The directory {path} does not exist.")
    state = check_vasp_dir_state(path)
    logger.opt(colors=True, raw=True).info(
        f"State: <{state.get_state_color()}>{str(state)}</>"
    )


def check_vasp_dirs_states_cli(
    root_dir: Path = ".",
    pattern: str = "job-*",
    skip_info_file: str = "tepkit.skip.info.toml",
    group: int = 50,
    list_mode: bool = False,
) -> None:
    """
    Check the states of a series of VASP jobs.

    :param root_dir: The path of the jobs' directory.
    :param pattern: The name pattern of the jobs' directory.
    :param skip_info_file: The name of the skip info file.
    :param group: The number of jobs to display in each line.
    :param list_mode: List mode

    :typer root_dir       flag: --root, -r
    :typer pattern        flag: --pattern, -p
    :typer skip_info_file flag: --skip-info-file, -s
    :typer group          flag: --group, -g
    :typer list_mode      flag: --list, -l
    """
    from tqdm import tqdm

    root_path = Path(root_dir).resolve()
    job_paths = sorted(root_path.glob(pattern))

    if len(job_paths) == 0:
        logger.warning(
            f"No job directory found in {root_path} with pattern {pattern}, program exit."
        )
        exit()

    states = {}
    for job_path in tqdm(
        job_paths,
        bar_format=R"{l_bar}{bar}| [{n_fmt:>3}/{total_fmt:>3} Jobs Checked]",
        leave=False,
    ):
        state = check_vasp_dir_state(job_path)
        if state is VaspState.Finished:
            state_symbol = "#"
        elif (job_path / skip_info_file).exists():
            state_symbol = "S"
        elif state is VaspState.Uncompleted:
            state_symbol = "R"
        else:
            state_symbol = "_"
        states[job_path] = state_symbol

    state_symbols = list(states.values())
    status_text = "".join(state_symbols)
    status_count = {
        "finished": state_symbols.count("#") + state_symbols.count("S"),
        "unfinished": len(status_text) - state_symbols.count("#"),
        "running": state_symbols.count("R"),
        "unstarted": state_symbols.count("_"),
    }

    def progress_bar(current, maximum, bar_length=50):
        progress = int((current / maximum) * bar_length)
        precent = str(int(current / maximum * 100))
        bar = "[" + "#" * progress + "_" * (bar_length - progress) + "]"
        return f"{bar} {precent} % ({current} / {maximum})"

    def format_text(_text, _group=group):
        result = []
        last_job_num = len(_text)
        for i in range(0, last_job_num, _group):
            start_index = i
            end_index = min(i + _group, last_job_num)
            line = f"{start_index + 1:03} {_text[start_index:end_index]} {end_index:03}"
            result.append(line)
        return "\n".join(result)

    print("Total Progress")
    print(progress_bar(status_count["finished"], len(status_text)))
    if list_mode:
        print("-" * 12 + " Details " + "-" * 12)
        i = 1
        for path, state_symbol in states.items():
            print(f"{i:4}: [{state_symbol}] {path}")
            if i % group == 0:
                print("-" * 33)
            i += 1
    else:
        print("Detailed Progresses")
        print(format_text(status_text))
