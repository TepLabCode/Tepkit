# Tepkit

**Tepkit** is a user-friendly program for accelerating
the calculation and analysis processes of 
transport, electronic, and thermoelectric properties of materials.

- Documentation: [Home | Tepkit Documentation](https://teplabcode.github.io/TepkitDoc/)
- API Reference: [API Reference | Tepkit Documentation](https://teplabcode.github.io/TepkitDoc/others/api_reference_overview.html)

## How To Cite

If you have used Tepkit in your work, please cite our paper
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
> 
> Or, you can install most possible required packages by running:
> 
> ```bash
> pip install .[all]
> ```

## Installation

### 1. Download the package

Go to the [releases page](https://github.com/TepLabCode/Tepkit/releases), and download the latest release:

`tepkit-<version>.tar.gz`

### 2. Extract

Use the command or any other tool to extract the file.

```bash
tar -xvf tepkit-*.tar.gz
```

### 3. (Optional) Create Conda Environment

You can use conda to create a virtual environment with Python 3.11 for Tepkit.

```bash
conda create --name tepkit python=3.11
conda activate tepkit
```

If you have not installed it, you can install one of the following:

- [Anaconda](https://www.anaconda.com/download)
- [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main)

### 4. Install Tepkit

Cheak if your Python version is at least 3.11 by:

 ```bash
 python --version
 # Python 3.11.x
 ```

If your Python version is less than 3.11, and you do not want or cannot change it, check step 3.

Go to the extracted directory and install the package by pip:

```bash
cd tepkit-*
pip install .
```

## Usage

You can use Tepkit as a command-line interface (CLI) in the console.

```bash
> tepkit
```

If you installed Tepkit in conda:

```bash
> conda activate tepkit
> tepkit
```

Or you can use Tepkit as a Python module:

```python
import tepkit
```

## About Name

**Tepkit** is a python package to assist with the first principles calculations.

- It is a **T**ransport and **E**lectronic **P**roperties Tool**kit**.

- It is also a **T**hermo**E**lectric **P**roperties Tool**kit**.
