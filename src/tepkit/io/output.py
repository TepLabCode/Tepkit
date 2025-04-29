from pathlib import Path

import pandas as pd

from tepkit.utils.typing_tools import PathLike


def save_df(
    df: pd.DataFrame,
    to_path: PathLike,
    fmt: str = "auto",
):
    match fmt.lower():
        case "auto":
            ext = Path(to_path).suffix
        case "csv":
            ext = ".csv"
        case "xlsx" | "excel":
            ext = ".xlsx"
        case "pickle":
            ext = ".pickle"
        case _:
            raise ValueError(f"Unsupported Format {fmt}")
    save_path = Path(to_path).with_suffix(ext)
    match ext:
        case ".csv":
            df.to_csv(save_path)
        case ".xlsx":
            df.to_excel(save_path)
        case ".pickle":
            df.to_pickle(save_path)
        case _:
            raise ValueError(f"Unsupported File Extension {ext}")
