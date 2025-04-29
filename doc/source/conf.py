# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Tepkit"
copyright = "2024–2025, TepLab"
author = "TepLab"
release = "1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    # "sphinx.ext.doctest",
    # "sphinx.ext.intersphinx",
    # "sphinx.ext.todo",
    # "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    # "sphinx.ext.ifconfig",
    # "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    # "sphinx.ext.napoleon",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = []

locale_dirs = ["locale/"]  # path is example but recommended.
gettext_compact = False  # optional.

suppress_warnings = ["toc.duplicated"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

# Custom
html_title = "Tepkit Documentation"
add_module_names = False

autodoc_member_order = "bysource"
autodoc_default_options = {
    "undoc-members": False,
    "autoclass_content": "both",
    "toc_object_entries_show_parents": "hide",
}

# Theme
html_theme = "sphinx_book_theme"

# AutoAPI
extensions.append("autoapi.extension")
autoapi_dirs = ["../../src/tepkit"]
autoapi_template_dir = "../templates/autoapi"
autoapi_options = [
    "members",
    # "inherited-members",
    "undoc-members",
    # "private-members",  # Display private objects (eg. _foo in Python)
    "show-inheritance",
    # "show-inheritance-diagram",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_add_toctree_entry = False
autoapi_own_page_level = "class"
autoapi_keep_files = True
suppress_warnings += ["autoapi.python_import_resolution"]
exclude_patterns += [
    "autoapi/tepkit/index.rst",
    "autoapi/tepkit/cli/*",
    "autoapi/tepkit/config/*",
]
# autoapi_member_order = "groupwise"


def autoapi_prepare_jinja_env(jinja_env):
    def replace_typehint(value):
        value = value.replace("tepkit.utils.typing_tools.", "")
        return value

    jinja_env.filters["replace_typehint"] = replace_typehint


def skip_util_classes(app, what, name, obj, skip, options):
    if "logger" in name:
        skip = True
    if what == "package" and "functions" in name:
        skip = True
    if "autoapi_skip" in name:
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_util_classes)


# Markdown
extensions.append("myst_parser")
