def add(a: float, b: float):
    """
    The simplest example.

    Add two float.

    :typer a argument:
    :typer b argument:
    """
    print(f"{a} + {b} = {a+b}")


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
