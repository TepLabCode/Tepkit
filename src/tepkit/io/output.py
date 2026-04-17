from pathlib import Path

import pandas as pd

from tepkit.utils.typing_tools import PathLike


def save_df(
    df: pd.DataFrame,
    to_path: PathLike,
    fmt: str = "auto",
):
    """
    Save a DataFrame in the selected format.
    
    [zh-CN]
    以指定格式将 DataFrame 保存到文件。
    
    :param df: DataFrame to save.
    :param to_path: Target path or stem.
    :param fmt: Output format.
    :return: ``None``.
    
    """
    # Resolve the target file extension.
    # 根据请求的格式解析目标扩展名。
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
