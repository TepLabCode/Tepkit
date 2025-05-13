# Installation

## Step 1 — Prepare the Environment

### Method A: In conda environment (Recommended)

You can use conda to create a virtual environment with Python 3.11 for Tepkit.

```bash
conda create --name tepkit python=3.11
conda activate tepkit
```

If you have not installed it, check one of the following:

- [Anaconda](https://www.anaconda.com/download)
- [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main)

### Method B: In native environment

Cheak if you have installed [Python](https://www.python.org), and check if the version is **at least 3.11** by:

## Step 2 — Install Tepkit

### Method A: Form PyPI (Recommended)

```bash
pip install tepkit
```

### Method B: From GitHub

```bash
pip install git+https://github.com/TepLabCode/Tepkit.git
```

### Method C: From Releases

1. **Download**:  
   Go to the [releases page](https://github.com/TepLabCode/Tepkit/releases),
   and download the latest released package:  
   `tepkit-<version>.tar.gz`
2. **Extract**:  
   Extract the package by command or any other tool you like.  
   ( Example command: `tar -xvf tepkit-*.tar.gz` )
3. **Install**:
   Go to the extracted directory and install the package:  
   ```bash
   cd tepkit-*
   pip install .
   ```
### (Optional) Install All Dependencies

By default, Tepkit will only install the basic dependencies,  
so you may meet `ModuleNotFoundError` when running some commands or using some functions.

If you want to install all dependencies at once,  
you can add the `[all]` option to the installation command, like:

```bash
pip install tepkit[all]
```

## Step 3 — Test

### A. As a Command-line Interface (CLI)

You can test if Tepkit is installed correctly by running the `tepkit` command in the console.

```bash
> tepkit
```

If you installed Tepkit in conda, you need to activate the environment before running the command:

```bash
> conda activate tepkit
> tepkit
```

### B. As a Python Module

You can test if Tepkit can be imported correctly by the following code in Python:

```python
import tepkit
```