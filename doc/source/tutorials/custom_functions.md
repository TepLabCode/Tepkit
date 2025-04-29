# How to Add Custom Functions


## Basic

1. Use `tepkit -w` to check the path of Tepkit package.
2. Go to `tepkit/functions/custom/`
3. Create a new Python file containing your custom function.
    like: `my_functions.py`
    ```python
    # my_functions.py
    def my_minus(a, b):
        return a - b
    ```
4. Then, open `tepkit/functions/custom/__init__.py`, and edit the `custom_commands_data` dict.
    ```python
    custom_commands_data = [
        {
            "command_names": ["add"],
            "function_module": "tepkit.functions.custom.example",
            "function_name": "add",
        },
        {
            "command_names": ["hi", "hello"],
            "function_module": "tepkit.functions.custom.example",
            "function_name": "hello",
        },
        # ↓↓↓ Add your custom function here ↓↓↓
        {
            "command_names": ["minus"],
            "function_module": "tepkit.functions.custom.my_functions",
            "function_name": "my_minus",
        },
    ]
    ```
5. Then, you can run `tepkit custom` to see if your custom function is added properly.
6. Try to run `tepkit custom minus -h` and `tepkit custom minus --a 1 --b 2` to see if your custom function works.

## Advanced

Tepkit use a unique method to config typer command configuration by docstring.

- Use Python type hint to define the parameter type: `def my_func(a: int, b: float): ...`
- Add help to a parameter: `:param a: first number`
- change the callname or add a alias to a parameter:
  - `:typer a flag: --first, --alpha, -a`
- make a parameter from option to argument: `:typer a argument:`
- change the metavar of a parameter: `:typer a metavar: number`
- group the parameters in a panel: `:typer a panel: Panel1`

A detailed example `hello()` are shown in `tepkit/functions/custom/example.py`

```python
def hello(
    first_name: str,
    last_name: str,
    middle_name: str = None,
):
    """
    A more complete example.

    you can use a reST style docstring to specify
    the "help" "metavar" "flag" and "panel" of the arguments,
    and use the "&" symbol at the end of a line
    to write a multi-line help.

    :param first_name : your first name &
                        or given name.
    :param middle_name: your middle name.
    :param last_name  : your last name &
                        or family name.

    :typer first_name  metavar: NAME
    :typer middle_name metavar: NAME
    :typer last_name   metavar: NAME

    :typer first_name  flag: --first-name,  --fn, -f
    :typer middle_name flag: --middle-name, --mn, -m
    :typer last_name   flag: --last-name,   --ln, -l

    :typer middle_name panel: Optional Flags
    """
    if middle_name:
        print(f"Hello, {first_name} {middle_name} {last_name}!")
    else:
        print(f"Hello, {first_name} {last_name}!")
```

It will show like below:

```
> tepkit custom -i hello -h

 Usage: tepkit custom hello [OPTIONS]

 A more complete example.
 ──────────────────────────────
 you can use a reST style docstring to specify
 the "help" "metavar" "flag" and "panel" of the arguments,
 and use the "&" symbol at the end of a line
 to write a multi-line help.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ *  --first-name,--fn  -f      NAME  your first name [default: None] [required]     │
│                                     or given name.                                 │
│ *  --last-name,--ln   -l      NAME  your last name  [default: None] [required]     │
│                                     or family name.                                │
│    --help             -h            Show this message and exit.                    │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭─ Optional Flags ───────────────────────────────────────────────────────────────────╮
│ --middle-name,--mn  -m      NAME  your middle name. [default: None]                │
╰────────────────────────────────────────────────────────────────────────────────────╯
```
