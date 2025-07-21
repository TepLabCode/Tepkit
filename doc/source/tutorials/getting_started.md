# Getting Started

After you have successfully [installed the package](installation.md),
we can try to use it!

## As a Command-line Interface (CLI)

First, let's open the console and type `tepkit`.

```bash
> tepkit
``` 

You will see the following message:

```
===== Tepkit Info =====
 Version : 0.2.0
 Location: /path/to/tepkit
===== Tepkit Help =====

 Usage: tepkit [OPTIONS] COMMAND [ARGS]...

 Welcome to Tepkit!
 ──────────────────────────────
 Note: The command number (c__) may change with the version,
 please use the full name when using tepkit in your script.

╭─ Options ────────────────────────────────────────────────────────────╮
│ --version    -v             Show the version of Tepkit.              │
│ --where      -w             Show the path of Tepkit package.         │
│ --log-level          LEVEL  Set the log level of current execution.  │
│                             [default: 18]                            │
│ --help       -h             Show this message and exit.              │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────╮
│ c01 | vasp                 VASP tools.                               │
│ c02 | phonopy              Phonopy tools.                            │
│ c03 | 3ord | thirdorder    thirdorder tools.                         │
│ c04 | 4ord | fourthorder   fourthorder tools.                        │
│ c05 | shengbte             ShengBTE tools.                           │
│ c06 | sym                  symmetry tools.                           │
│ c99 | custom               Custom functions.                         │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Functions ──────────────────────────────────────────────────────────╮
│ f01 | dp                   Calculate carrier mobility and relaxation │
│                            time using DP method.                     │
╰──────────────────────────────────────────────────────────────────────╯
```

**Left** is the **command names**,  
**Right** is the **command descriptions**.

The symbols `|` separates the aliases of the same command,  
which means `tepkit c03` `tepkit 3ord` and `tepkit thirdorder` are exactly the same command.

**Functions** panel contains each specific function.  
**Commands** panel contains the groups of function.

You can type `tepkit <group_name>` to go to the sub-menu of tepkit:

```bash
> tepkit phonopy
```

```
 Usage: tepkit phonopy [OPTIONS] COMMAND [ARGS]...

 Phonopy tools.

╭─ Options ────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Functions ──────────────────────────────────────────────────────────╮
│ rms   Calculate and Plot the root-mean-square (RMS) of               │
│       FORCE_CONSTANTS.                                               │
╰──────────────────────────────────────────────────────────────────────╯
```

And you can always use `--help` or `-h` to check the usage of each command or function.

```bash
> tepkit phonopy rms -h
```

```
 Usage: tepkit phonopy rms [OPTIONS]

 Calculate and Plot the root-mean-square (RMS) of FORCE_CONSTANTS.
 ──────────────────────────────
 Required Files:
 | FORCE_CONSTANTS
 | SPOSCAR
 Output Files:
 | tepkit.RMS_of_2ndIFCs.csv
 | tepkit.RMS_of_2ndIFCs.png

╭─ Options ────────────────────────────────────────────────────────────╮
│ --work-dir      -d              PATH  The directory where the        │
│                                       required files is located.     │
│                                       [default: ./]                  │
│ --fc                            TEXT  The name of the                │
│                                       FORCE_CONSTANTS file.          │
│                                       [default: FORCE_CONSTANTS]     │
│ --sposcar,--sc                  TEXT  The name of the SPOSCAR file.  │
│                                       [default: SPOSCAR]             │
│ --save-dir                      PATH  The directory where the output │
│                                       files will be saved.           │
│                                       (`--save-dir work_dir` will    │
│                                       save the files to `work_dir`)  │
│                                       [default: ./]                  │
│ --save-name     -s              TEXT  The name of the output files.  │
│                                       [default: Auto]                │
│ --fit               --no-fit          [default: no-fit]              │
│ --help          -h                    Show this message and exit.    │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Plot Settings ──────────────────────────────────────────────────────╮
│ --plot    --no-plot             Whether to plot the figure of data.  │
│                                 [default: plot]                      │
│ --nth     --no-nth              Show the distances of the atoms'     │
│                                 n-th neighbor.                       │
│                                 [default: nth]                       │
│ --log     --linear              Set the y-axis to logarithmic        │
│                                 coordinates.                         │
│                                 [default: linear]                    │
│ --xlim                 MIN MAX  The range of the x-axis.             │
│                                 [default: Auto, Auto]                │
│ --ylim                 MIN MAX  The range of the y-axis.             │
│                                 [default: Auto, Auto]                │
╰──────────────────────────────────────────────────────────────────────╯
```

### Example: Convert `POSCAR` to ShengBTE input file `CONTROL`

Try to type the following command, and it will convert the `POSCAR`
file at current directory to `CONTROL` format:

```bash
> tepkit shengbte control
```

If `POSCAR` is located at another directory or has a different name,
you can use the `--poscar PATH` option to specify the file:

```bash
> tepkit shengbte control --poscar /path/to/POSCAR.vasp
```

You can use the `--help / -h` option to find more detail options:

```
> tepkit shengbte control -h

 Usage: tepkit shengbte control [OPTIONS]

 generate the CONTROL file from POSCAR file.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --poscar             -p      PATH           Path of POSCAR file                    │
│                                             [default: ./POSCAR]                    │
│ --temperature        -t      INT            Single value of temperature (priority) │
│                                             [default: None]                        │
│ --temperatures,--ts          [INT INT INT]  [T_min, T_max(include), T_step]        │
│                                             [default: None, None, None]            │
│ --ngrid              -n      [INT INT INT]  Value of ngrid [default: 1, 1, 1]      │
│ --supercell,--sc             [INT INT INT]  Supercell of FORCE_CONSTANTS_2ND       │
│                                             [default: 1, 1, 1]                     │
│ --path                       PATH           Save path of CONTROL file              │
│                                             [default: ./CONTROL]                   │
│ --help               -h                     Show this message and exit.            │
╰────────────────────────────────────────────────────────────────────────────────────╯
```

Thus, you can specify the `ngrid` `supercell` and `temperature` options in the `CONTROL` file.

Here is a complete example of this command:

```bash
> tepkit shengbte control --poscar /path/to/POSCAR.vasp --ngrid 56 56 1 --sc 3 3 1 -t 300
```

## As a Python Module

You can also use Tepkit as a Python module in your own Python scripts.

```python
import tepkit
```

### Using Tepkit CLI Commands in Script

If you want to use a CLI command in your Python script,
you can check the `tepkit.cli.typer.commands_data.builtin_groups_data` module,
and find the `group_module` and `function_name`of the desired command.

```python
from rich import print
from tepkit.cli.typer.commands_data import builtin_groups_data
print(builtin_groups_data)
```

For example, if you want to use the `tepkit shengbte control` command,
you can find:

```
    {
        'group_names': ['c05', 'shengbte'],
        'group_module': 'tepkit.functions.shengbte',
        'group_help': 'ShengBTE tools.',
        'sub_commands': [
            {
                'command_names': ['control'],
                'function_name': 'poscar_to_control'
            }
        ]
    },
```

which means the `tepkit shengbte control` command is the `poscar_to_control()` function
in the `tepkit.functions.shengbte` module,
and you can use it as follows:

```python
from tepkit.functions.shengbte import poscar_to_control

poscar_to_control(
    poscar = "./POSCAR",
    temperature = 300,
    ngrid = (56, 56, 1),
    supercell = (3, 3, 1),
    path = "./CONTROL",
)
```

### Prase and process the files

One of Tepkit's core functions is to parse files from different software.

You can find the supported file formats at [this page](../file/_overview.md),

Here is an example of parsing `vasp` files:

1. Import the class of your desired file format:

    ```python
    from tepkit.io.boltztrap2 import Condtens
    ```

2. Read the file by directory:

    ```python
    # Default file name is "interpolation.condtens"
    condtens = Condtens.from_dir(R".\input-boltztrap2")
    ```

    ```python
    # Specify the file name
    condtens = Condtens.from_dir(R".\input-boltztrap2", file_name="xxx.condtens")
    ```

    or by file path:

    ```python
    condtens = Condtens.from_file(R".\input-boltztrap2\interpolation.condtens")
    ```

3. Get the data table:

    ```python
    import pandas as pd
    df: pd.DataFrame = condtens.df
    print(df)
    ```

    most data tables in Tepkit have three column indices:

    - `quantity`: the name/symbol of the quantity, like `T` and `sigma/tau`
    - `unit`: the unit of the quantity, like `K` and `S/(m*s)`
    - `direction`: the direction of the vector/tensor, like `x` and `xx`
   
    You can get one specific column by: `df[("sigma/tau", "S/(m*s)", "xx")]`,  
    or get the tensor table by `df[("sigma/tau", "S/(m*s)")]`

4. Thus, you can easily analyze the data by any other Python libraries, like `numpy` and `matplotlib`.  
   Note: You can find many reference codes in our [example scripts](https://github.com/TepLabCode/Tepkit/tree/main/examples).


