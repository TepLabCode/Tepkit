from importlib import metadata
from pathlib import Path

current_file_path = Path(__file__).resolve()
package_root = current_file_path.parent
paths = {"test_files": package_root.parent.parent / "tests" / "test_files"}


try:
    __version__ = metadata.version("tepkit")
except metadata.PackageNotFoundError:
    __version__ = "Unknown"
