# Usage:
# ```bash
# pip install .
# ```

from pathlib import Path

import numpy
import spglib
from Cython.Build import cythonize
from setuptools import Extension, setup

# Get the paths of `numpy` and `spglib`
# numpy
numpy_include_dir = numpy.get_include()
# spglib
spglib_include_dir = str(Path(spglib.__file__).parent / "include")
for spglib_subdir in ["lib", "lib64"]:
    spglib_library_dir = Path(spglib.__file__).parent / spglib_subdir
    if spglib_library_dir.exists():
        spglib_library_dir = str(spglib_library_dir)
        break
else:
    raise FileNotFoundError(
        "Can not find spglib_library_dir, please manually input it in `setup.py`."
    )

# Manually input
# spglib_include_dir = "/path/to/spglib.h"
# spglib_library_dir = "/path/to/symspg.dll_or_libsymspg.so"

# Define the extension module
ext_modules = [
    Extension(
        name="thirdorder_core",
        sources=["thirdorder_core.pyx"],
        include_dirs=[
            numpy_include_dir,  # numpy header files
            spglib_include_dir,  # spglib header files
        ],
        library_dirs=[
            spglib_library_dir,  # spglib library files
        ],
        libraries=[
            "symspg",  # the library name of spglib
        ],
    )
]

setup(
    name="thirdorder_core",  # Package name
    version="1.0.0",  # Package version
    # Cythonize the extension module
    ext_modules=cythonize(
        ext_modules,
    ),
)
