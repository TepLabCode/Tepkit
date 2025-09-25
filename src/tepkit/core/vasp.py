from enum import StrEnum
from pathlib import Path


class VaspState(StrEnum):
    """
    VASP State Enum.
    """

    Unstarted = "Unstarted"
    """OUTCAR file does not exist."""
    Uncompleted = "Uncompleted"
    """OUTCAR file exists but no end information."""
    Finished = "Finished"
    """OUTCAR file exists and has end information."""

    def __bool__(self):
        return self == VaspState.Finished

    def get_state_color(self) -> str:
        match self:
            case VaspState.Unstarted:
                return "light-white"
            case VaspState.Uncompleted:
                return "orange"
            case VaspState.Finished:
                return "green"


def check_vasp_dir_state(path=".") -> VaspState:
    """
    Check the state of a VASP calculation by OUTCAR.

    [zh-CN]
    利用 OUTCAR 文件检查 VASP 计算的状态。

    OPTIMIZE: 可以考虑只读取 OUTCAR 的末尾来优化性能，
              但是目前不确定是否关键词确实只出现在最后，
              暂且保留目前的全读取方法。
    """
    path: Path = Path(path).resolve()
    outcar_path: Path = path / "OUTCAR"
    if not outcar_path.exists():
        return VaspState.Unstarted
    with outcar_path.open("r") as f:
        content = f.read()
        if "General timing and accounting informations for this job" in content:
            return VaspState.Finished
        else:
            return VaspState.Uncompleted
