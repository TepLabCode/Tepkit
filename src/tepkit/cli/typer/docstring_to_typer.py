from typing import Annotated

import typer
from docstring_parser import parse


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
    docstring = parse(func.__doc__)
    type_hints = func.__annotations__
    metas = get_docstring_metas(docstring, "typer")

    # typer.OptionInfo
    for arg, type_hint in type_hints.items():
        # Get DocString Settings
        option_settings = metas.get(arg, {})
        # Get typer.OptionInfo
        if not hasattr(type_hint, "__metadata__"):
            if "argument" in option_settings:
                type_hints[arg] = Annotated[type_hint, typer.Argument()]
            else:
                type_hints[arg] = Annotated[type_hint, typer.Option()]
        typer_option_info = type_hints[arg].__metadata__[0]
        # Help Message
        docstring_helps = {
            param.arg_name: param.description.replace("&\n", "\n\n")
            for param in docstring.params
        }
        typer_option_info.help = docstring_helps.get(arg)
        # Basic Settings
        typer_option_info.metavar = option_settings.get("metavar")
        typer_option_info.rich_help_panel = option_settings.get("panel")
        typer_option_info.hidden = "hidden" in option_settings
        # click.Choice
        typer_option_info.case_sensitive = (
            option_settings.get("case_sensitive") == "True"
        )
        # click.Path
        typer_option_info.exists = option_settings.get("exists") == "True"
        # CLI Flags
        flags = option_settings.get("flag", tuple())
        if len(flags) >= 1:
            typer_option_info.default = flags[0]
        if len(flags) >= 2:
            typer_option_info.param_decls = flags[1:]
    func.__annotations__ = type_hints

    # Function Description
    doc_parts = [docstring.short_description or ""]
    if docstring.long_description:
        doc_parts += [
            "",
            "─" * 30,
            docstring.long_description,
        ]
    func.__doc__ = "\n".join(doc_parts)

    return func
