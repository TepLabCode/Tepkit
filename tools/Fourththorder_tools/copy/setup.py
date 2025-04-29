# Usage:
# ```bash
# pip install .
# ```
# If it failed, try:
# ```bash
# python setup.py clean --all
# python setup.py build_ext --inplace
# python setup.py install
# ```

from pathlib import Path

import numpy
import spglib
import Cython
from Cython.Build import cythonize
from setuptools import Extension, setup

# Get the paths of `numpy` and `spglib`
numpy_include_dir = numpy.get_include()
spglib_include_dir = str(Path(spglib.__file__).parent / "include")
spglib_library_dir = str(Path(spglib.__file__).parent / "lib")

# Increase buff_max_dims to avoid Cython error
Cython.Compiler.Options.buffer_max_dims = 10

# Define the extension module
ext_modules = [
    Extension(
        name="Fourthorder_core",
        sources=["Fourthorder_core.pyx"],
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
    name="Fourthorder_core",  # Package name
    version="1.0.0",  # Package version
    # Cythonize the extension module
    ext_modules=cythonize(
        ext_modules,
        language_level=2,  # Set the language level to Python 2.7
    ),
)
