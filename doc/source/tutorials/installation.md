# Installation

## Steps

### 1. Download the package

Go to the [releases page](https://github.com/TepLabCode/Tepkit/releases), and download the latest release:

`tepkit-<version>.tar.gz`

### 2. Extract

Use the command or any other tool to extract the file.

```bash
tar -xvf tepkit-*.tar.gz
```

### 3. (Optional) Create Conda Environment

```bash
conda create --name tepkit python=3.11
conda activate tepkit
```

### 4. Install Tepkit

Cheak your Python version by:

 ```bash
 python --version
 # Python 3.11.x
 ```

If your Python version is less than 3.11, and you do not want to change it, check step 3.

Go to the extracted directory and install the package by pip:

```bash
cd tepkit-*
pip install .
```

## Test

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