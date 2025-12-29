"""
This module provides classes for MLIP package developed by Alexander Shapeev et al.
"""

from tepkit.io import StructuredTextFile
from tepkit.utils.typing_tools import Self


class MlipCfg(StructuredTextFile):

    def __init__(self):
        super().__init__()
        self.cfgs: list[str] = []

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Parse the string to structured data.
        """
        obj: Self = super().from_string(string)
        i_start = 0
        # noinspection PyTypeChecker
        for i, line in enumerate(obj.lines):
            if line.startswith("BEGIN_CFG"):
                i_start = i
            elif line.startswith("END_CFG"):
                obj.cfgs.append("\n".join(obj.lines[i_start : i + 2]))
        return obj

    def slice(self, _slice: slice, /) -> None:
        self.cfgs = self.cfgs[_slice]

    def to_string(self) -> str:
        return "\n".join(self.cfgs) + "\n"


if __name__ == "__main__":
    config = MlipCfg.from_file(R"C:\Users\Elnath\Downloads\test.cfg")
    config.slice(slice(0, 11))
    config.to_file("test.mlip.cfg")
