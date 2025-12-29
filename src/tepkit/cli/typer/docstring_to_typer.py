from typing import Annotated

import typer
from docstring_parser import parse
from typer.models import ParameterInfo


def update_dict(target, indexes, value):
    for i in indexes[:-1]:
        if i not in target:
            target[i] = {}
        target = target[i]
    if indexes[-1] == "flag":
        target[indexes[-1]] = tuple(value.replace(" ", "").split(","))
    else:
        target[indexes[-1]] = value
    return target


def get_docstring_metas(docstring, key) -> dict:
    result: dict = {}
    metas = [meta for meta in docstring.meta if meta.args[0] == key]
    if len(metas) > 0:
        for meta in metas:
            update_dict(result, meta.args, meta.description)
        return result[key]
    else:
        return {}


def docstring_to_typer(func):
    """
    Supported Typer ParameterInfo settings:
        # General
    [✓] default: Optional[Any] = None,
    [✓] param_decls: Optional[Sequence[str]] = None,
        callback: Optional[Callable[..., Any]] = None,
    [✓] metavar: Optional[str] = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: Optional[Union[str, List[str]]] = None,
        shell_complete: Optional[...] = None,
        autocompletion: Optional[Callable[..., Any]] = None,
        default_factory: Optional[Callable[[], Any]] = None,
        # Custom type
        parser: Optional[Callable[[str], Any]] = None,
        click_type: Optional[click.ParamType] = None,
        # TyperArgument
        show_default: Union[bool, str] = True,
        show_choices: bool = True,
        show_envvar: bool = True,
    [✓] help: Optional[str] = None,
    [✓] hidden: bool = False,
        # Choice
    [✓] case_sensitive: bool = True,
        # Numbers
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        clamp: bool = False,
        # DateTime
        formats: Optional[List[str]] = None,
        # File
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = "strict",
        lazy: Optional[bool] = None,
        atomic: bool = False,
        # Path
    [✓] exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Union[None, Type[str], Type[bytes]] = None,
        # Rich settings
    [✓] rich_help_panel: Union[str, None] = None,
    """
    docstring = parse(func.__doc__)
    type_hints = func.__annotations__
    metas: dict = get_docstring_metas(docstring, "typer")
    arg_helps = {
        param.arg_name: param.description.replace("&\n", "\n\n")
        for param in docstring.params
    }

    # Build typer.OptionInfo (or typer.ArgumentInfo)
    for param, type_hint in type_hints.items():
        # Get settings for this argument
        param_settings: dict = metas.get(param, {})

        # Get or Create `OptionInfo` or `ArgumentInfo`
        if not hasattr(type_hint, "__metadata__"):
            if "argument" in param_settings:
                type_hints[param] = Annotated[type_hint, typer.Argument()]
            else:
                type_hints[param] = Annotated[type_hint, typer.Option()]
        typer_param_info: ParameterInfo = type_hints[param].__metadata__[0]

        # Help Message
        typer_param_info.help = arg_helps.get(param)

        # Basic Settings
        typer_param_info.metavar = param_settings.get("metavar")
        # └ e.g. `:typer arg_name metavar: METAVAR`
        typer_param_info.rich_help_panel = param_settings.get("panel")
        # └ e.g. `:typer arg_name panel: Panel Name`
        typer_param_info.hidden = "hidden" in param_settings
        # └ e.g. `:typer arg_name hidden:`

        # ===== click.Choice ===== #
        typer_param_info.case_sensitive = (param_settings.get("case_sensitive") == "True")  # fmt: skip
        # └ e.g. `:typer arg_name case_sensitive: True`

        # ===== click.Path ===== #
        typer_param_info.exists = (param_settings.get("exists") == "True")  # fmt: skip
        # └ e.g. `:typer arg_name exists: True`

        # CLI Flags
        flags = param_settings.get("flag", tuple())
        if len(flags) >= 1:
            typer_param_info.default = flags[0]
        if len(flags) >= 2:
            typer_param_info.param_decls = flags[1:]

    # Reassign `__annotations__`
    func.__annotations__ = type_hints

    # Add blank line and separator into function docstring
    doc_parts = [docstring.short_description or ""]
    if docstring.long_description:
        doc_parts += [
            "",
            "─" * 30,
            docstring.long_description,
        ]
    # Reassign `__doc__`
    func.__doc__ = "\n".join(doc_parts)

    # Return the function
    return func
