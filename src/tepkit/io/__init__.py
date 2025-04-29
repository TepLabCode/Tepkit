"""
This package is used to read and write files of various formats.
"""

from pathlib import Path

from tepkit.utils.typing_tools import PathLike, Self
import pandas as pd


class File:
    """
    The base class for all files.
    """

    default_dir_path: PathLike = "./"
    "The default path of located directory of file when use ``from_dir()`` ."
    default_file_name: str = None
    "The default name of file when use ``from_dir()`` ."

    def __init__(self):
        self.source_path: Path | None = None
        """Record the path of the file when use ``from_file()`` or ``from_dir()`` ."""

    @classmethod
    def from_file(cls, path: PathLike) -> Self:
        """
        Read a file by its ``path`` .

        >>> file1 = File.from_file("example.txt")
        >>> file2 = File.from_file("../example.txt")
        """
        obj = cls()
        obj.source_path = Path(path)
        return obj

    @classmethod
    def from_dir(cls, path: PathLike = None, file_name: str = None) -> Self:
        """
        Read a file named ``cls.default_file_name`` in the ``cls.default_dir_path``.

        >>> file1 = File.from_dir()

        You can also specify the dirctory path or the file name:

        >>> file2 = File.from_dir("./result")
        >>> file3 = File.from_dir(file_name = "file_name.txt")
        >>> file4 = File.from_dir("./result", file_name = "file_name.txt")
        """
        dir_path = Path(path or cls.default_dir_path)
        file_name = file_name or cls.default_file_name
        if file_name is None:
            raise KeyError("file_name can not be None")
        else:
            file_path = dir_path / file_name
        return cls.from_file(file_path)

    @classmethod
    def to_file(cls, path: PathLike):
        """
        Write the data of the object to a file.
        """
        raise NotImplementedError(
            "The to_file() method of the file is not implemented now."
        )


class TextFile(File):
    """
    The class for text files.
    The base class for `StructuredTextFile` and `TableTextFile` .
    """

    def __init__(self):
        super().__init__()
        self.content: str | None = None
        """Record the string of the textfile."""

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Save the string to ``self.content`` and return the object.
        """
        obj = cls()
        obj.content = string
        return obj

    @classmethod
    def from_file(cls, path: PathLike) -> Self:
        """
        Read the text file, and save its text to self.content.
        """
        with open(path, "r") as file:
            obj = cls.from_string(file.read())
            obj.source_path = Path(path)
        return obj


class StructuredTextFile(TextFile):
    """
    The class for text file with special structure.
    """

    def __init__(self):
        super().__init__()
        self._lines: list[str] | None = None

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Parse the string to structured data.
        """
        obj = super().from_string(string)
        # === For subclass, add code here to parse the string ===
        ...
        # === End of subclass code ===
        return obj

    @classmethod
    def from_file(cls, path: PathLike) -> Self:
        """
        从文件中读取文本，然后调用 from_string 读取数据。
        """
        if not Path(path).is_file():
            raise FileNotFoundError(f"File {path} is not a file.")
        with open(path, "r") as file:
            obj = cls.from_string(file.read())
            obj.source_path = Path(path)
        return obj

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self.content.splitlines()
        return self._lines

    def to_file(self, path) -> None:
        with open(path, "w") as file:
            file.write(str(self))


class TableTextFile(TextFile):

    default_from_file_config = {
        "sep": r"\s+",
        "header": None,
        "skiprows": 0,
    }
    column_indices: dict = {"Index": []}
    column_indices_autofill: dict = {"prefix": "Column-", "start": 1}

    def __init__(self):
        super().__init__()
        self.df = None

    @classmethod
    def from_file(cls, path: PathLike = None):
        config = cls.default_from_file_config
        path = path or cls.default_file_name
        obj = super().from_file(path)
        df = pd.read_table(
            path,
            sep=config["sep"],
            header=config["header"],
            skiprows=config.get("skiprows", 0),
            dtype=config.get("dtype", None),
            index_col=config.get("index_col", None),
        )

        # Handle column indices
        if len(cls.column_indices) == 0:
            pass
        else:
            columns_names = list(cls.column_indices.keys())
            if cls.column_indices_autofill is not None:
                prefix = cls.column_indices_autofill.get("prefix", "")
                start = cls.column_indices_autofill.get("start", 1)
                suffix = cls.column_indices_autofill.get("suffix", "")
                column_indices = {}
                for name in columns_names:
                    # First, autofill all column names by format
                    column_indices[name] = [
                        f"{prefix}{str(start+i)}{suffix}"
                        for i in range(len(df.columns))
                    ]
                    # Then, override the column names with the values in cls.column_indices
                    for i, value in enumerate(cls.column_indices[name]):
                        column_indices[name][i] = value
            else:
                column_indices = cls.column_indices
            df.columns = list(column_indices.values())
            df.columns.names = columns_names
        obj.df = df

        # Return the object
        return obj


def array_to_string(
    array,
    fmt="% f",
    delimiter=" ",
    prefix="",
    suffix="",
) -> str:
    if fmt:
        if fmt == "bool_TF":
            formatted_array = ["T" if item else "F" for item in array]
        else:
            formatted_array = [fmt % element for element in array]
    else:
        formatted_array = [str(element) for element in array]

    result = prefix + delimiter.join(formatted_array) + suffix
    return result


def matrix_to_string(
    matrix,
    fmt="% f",
    delimiter=" ",
    line_prefix="",
    line_separator="\n",
    line_suffix="",
    prefix="",
    suffix="",
) -> str:
    lines = []
    for row in matrix:
        if fmt:
            formatted_row = [fmt % element for element in row]
        else:
            formatted_row = [str(element) for element in row]

        line = line_prefix + delimiter.join(formatted_row) + line_suffix
        lines.append(line)
    body = line_separator.join(lines)
    result = prefix + body + suffix
    return result
