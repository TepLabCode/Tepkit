# Documentation

This directory contains the documentation source files for the project.

## How to Build

```bash
cd doc
make html
```

Re-build all files:

```bash
cd doc
set set SPHINXOPTS=-a
make html
```

## About AutoAPI

We use AutoAPI to generate the API documentation, which can
generate documentation by parsing the source code.

See:

- Website:
  - [AutoAPI](https://autoapi.readthedocs.io/index.html)
  - [Sphinx AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/)
- Syntax
  - [sphinx.ext.autodoc — Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
  - [reStructuredText](https://docutils.sourceforge.io/rst.html)
  - [reStructuredText — Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)
  - [reStructuredText Primer — Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)

#### Header

- `#` with overline, for parts
- `*` with overline, for chapters
- `=` for sections
- `-` for subsections
- `^` for subsubsections
- `"` for paragraphs

## How to Preview

Directly open the `index.html` file in the `build/html` directory.

Or, run:

```bash
cd build/html
python -m http.server 8000
```

And then open the browser and go to http://localhost:8000/ .

## How to Auto-Build

- Ref: [Sphinx-Autobuild](https://sphinx-extensions.readthedocs.io/en/latest/sphinx-autobuild.html)

It can watch the source files and rebuild the documentation when any file changes,
and refresh the browser page to render the new changes.
```
cd doc
sphinx-autobuild source build/html 
```

# Internationalization

1. `make gettext` generate` doc/build/gettext` directory, 
   which contains all `*.pot` files needed for translation.
2. `sphinx-intl update -p build/gettext -l zh_CN` to update the `zh_CN` translation.
3. `sphinx-build -M html source zh_CN -D language=zh_CN` to build the documentation in Chinese.