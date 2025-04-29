# Work with thirdorder

`thirdorder` was originally developed based on Python2.  
Some of its contents have become less compatible with Python3.  
**Tepkit** provides some ways to make thirdorder more suitable for the current environment.

## Installation

The original installation script (`setup.py`) of thirdorder needs the `distutils` package to work.
However, `distutils` has been deprecated since Python 3.10 and been removed since Python 3.12. [^1]

**Tepkit** provides a new `setup.py` file which uses the more modern `setuptools` package to compile and install the `thirdorder` package.  
**You can find the scripts at `Tepkit/tools/thirdorder_tools/*`.**

In addition, our script can automatically obtain the pathes of the `spglib` libraries installed by python. You no longer need to find and fill the pathes in the script by yourself anymore.

How to use the scripts:

1. Download the lastest released version of thirdorder from the [release page](https://bitbucket.org/sousaw/thirdorder/downloads/?tab=tags), and extract it. **Or** clone the repository (`git clone https://bitbucket.org/sousaw/thirdorder.git`) to your local machine.
2. Replace the original `setup.py` and `cthirdorder_core.pxd` file with the ones by Tepkit.
3. Install the required packages of thirdorder by the command `pip install -r requirements.txt`.
4. Install thirdorder by the command `python setup.py install`.
5. The `thirdorder` package will be installed as `thirdorder_core` in the python site-packages directory.
6. Try the following code to test if the installation is successful.

**For Windows:**

```
import spglib
import os
spglib_dll_dir = os.path.dirname(spglib.__file__)
os.add_dll_directory(spglib_dll_dir)
import thirdorder_core
```
**For Linux:**

```
import spglib
import os
import ctypes
libsymspg_so_path = os.path.join(os.path.dirname(spglib.__file__), "lib", "libsymspg.so.2")
ctypes.cdll.LoadLibrary(libsymspg_so_path)
import thirdorder_core
```

You can also manually add the path of the required file [^2] to the environment variables, 

For linux:

```bash
export LD_LIBRARY_PATH=/path/to/spglib/lib:$LD_LIBRARY_PATH
```

For Windows:

- TODO


So that you can import thirdorder_core directly:


```
import thirdorder_core
```


## Run

### Step 1 - Generate Poscars

Original command:

```bash
python thirdorder_vasp.py sow 3 3 1 -3
```

Tepkit command:

```bash
tepkit thirdorder vasp_sow -a 3 3 1 -3
```

### Step 2 - Set Job Folders

Original command:

```bash
workdir="./jobs"
cp INCAR KPOINTS POTCAR ${workdir}
for i in 3RD.POSCAR.*
do
    d=${workdir}/job-${i##*.}
    mkdir $d
    mv $i $d/POSCAR
    ln -s ../INCAR ../KPOINTS ../POTCAR $d
done
```

Tepkit command:

```bash
tepkit thirdorder set_jobs --to ./jobs
```

### Step 3 - Check Duplicate Jobs

```bash
tepkit thirdorder check_dupl --dir jobs
```

### Step 4 - Run Jobs

TODO

### Step 5 - Get Results

Original command:

```bash
find job* -name vasprun.xml | sort -n | python thirdorder_vasp.py reap 3 3 1 -3
```

Tepkit command:

```bash
tepkit thirdorder vasp_reap -a 3 3 1 -3 --pattern job*
```

[^1]: [distutils — Building and installing Python modules — Python 3.13.2 documentation](https://docs.python.org/3/library/distutils.html)

[^2]: For Windows, it's `symspg.dll`. For Linux, it's `libsymspg.so.2`.

