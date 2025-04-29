"""
This module modifies loguru.logger to add custom levels and color output support.

The custom levels are:
- `STEP`: used to indicate a step is started.
- `DONE`: used to indicate an operation is done.
- `NOTE`: used to indicate some things that need attention.

Example usage:
```python
from tepkit.cli import logger
# no-color mode
logger.info("This is an info message.")
logger.step("This is a step message.")
logger.done("This is a done message.")
logger.note("This is a note message.")
# color mode (logger.color or logger.c for short)
logger.c.info("This is an <light-white>info</> message.")
logger.c.step("This is a <white>step</> message.")
logger.c.done("This is a <light-green>done</> message.")
logger.c.note("This is a <light-yellow>note</> message.")
```
"""

import sys
import types

from loguru import logger

from tepkit.config import get_config

custom_levels = {
    # "TRACE":    {"no":  5, "color": "<cyan><bold>"},    # ↓ Not Important
    # "DEBUG":    {"no": 10, "color": "<blue><bold>"},    # |
    "STEP":       {"no": 18, "color": "<white>"},         # | (Default Level)
    # "INFO":     {"no": 20, "color": "<bold>"},          # |
    # "SUCCESS":  {"no": 25, "color": "<green><bold>"},   # |
    "DONE":       {"no": 25, "color": "<light-green>"},   # |
    "NOTE":       {"no": 28, "color": "<light-yellow>"},  # |
    # "WARNING":  {"no": 30, "color": "<yellow><bold>"},  # |
    # "ERROR":    {"no": 40, "color": "<red><bold>"},     # |
    # "CRITICAL": {"no": 50, "color": "<RED><bold>"},     # ↓ Important
}  # fmt: skip


def add_method(target, level_name):
    def method(self, *args, **kwargs):
        return self.log(level_name, *args, **kwargs)

    setattr(
        target,
        level_name.lower(),
        types.MethodType(method, target),
    )


# Get Config
config = get_config()

# logger Initialization
logger.remove()
logger.add(
    sys.stdout,
    format=config["loguru"]["format"],
    level=config["loguru"]["log_level"],
)
logger_color = logger.opt(colors=True)

# Add New Levels
for name, level_config in custom_levels.items():
    logger.level(name, no=level_config["no"], color=level_config["color"])
    add_method(logger, name)
    add_method(logger_color, name)

# Create Shortcut logger.color and logger.c
setattr(
    logger,
    "color",
    logger_color,
)

setattr(
    logger,
    "c",
    logger_color,
)

# Add Type Hint
logger: type(logger)

# @deprecated("`logger_c` is deprecated, use `logger.color` or `logger.c` instead.")
logger_c = logger_color
