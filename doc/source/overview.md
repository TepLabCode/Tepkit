# Overview

**Tepkit** is a user-friendly program for accelerating
the calculation and analysis processes of 
transport, electronic, and thermoelectric properties of materials.

## How To Cite

If you have used phonopy in your work, please cite our paper
which indeed helps the Tepkit project to continue:

- *In preparation*

> ✏️ Some examples described in the paper are available in the `examples/paper_examples` directory.

## Requirements

As of now, this package is only supported on `Python >= 3.11`.  

The following libraries are required to run basic functions and will be installed automatically:

- `typer` & `docstring_parser` for Command-Line Interface (CLI)
- `loguru` & `tqdm`for Logging
- `toml` for Configuration File
- `numpy` & `scipy` for Mathmatical Calculations
- `pandas` for Table Data Handling
- `matplotlib` for Plotting

> ⚠️ Some commands may require additional packages, if you get a `ModuleNotFoundError` while running,
> try to install it by pip and then re-run the command.

## About Name

**Tepkit** is a python package to assist with the first principles calculations.

- It is a **T**ransport and **E**lectronic **P**roperties Tool**kit**.

- It is also a **T**hermo**E**lectric **P**roperties Tool**kit**.
