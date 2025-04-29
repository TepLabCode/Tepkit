import matplotlib.font_manager as fm
from loguru import logger

RECOMMENDED_SERIF_FONTS = [
    "Times New Roman",  # Windows
    "FreeSerif",  # Linux
    "DejaVu Serif",  # matplotlib
]
RECOMMENDED_SANS_FONTS = [
    "Helvetica",  # Recommended
    "Arial",  # Windows
    "FreeSans",  # Linux
    "DejaVu Sans",  # matplotlib
]
RECOMMENDED_MONO_FONTS = [
    "Consolas",  # Windows
    "FreeMono",  # Linux
    "DejaVu Sans Mono",  # matplotlib
]
RECOMMENDED_SERIF_FONTS_HANS = [
    "Source Han Serif SC",  # 思源宋体（简体中文优先）
    "Source Han Serif CN",  # 思源宋体（仅简体中文）
    "SimSun",  # 宋体（Windows）
]
RECOMMENDED_SANS_FONTS_HANS = [
    "Source Han Sans SC",  # 思源黑体（简体中文优先）
    "Source Han Sans CN",  # 思源黑体（仅简体中文）
    "Microsoft YaHei",  # 微软雅黑（Windows）
]

STYLE_TO_RECOMMENDED_FONTS = {
    "Serif": RECOMMENDED_SERIF_FONTS,
    "Sans": RECOMMENDED_SANS_FONTS,
    "Mono": RECOMMENDED_MONO_FONTS,
    "Serif-Hans": RECOMMENDED_SERIF_FONTS_HANS,
    "Sans-Hans": RECOMMENDED_SANS_FONTS_HANS,
}


def is_font_avalible(font_name: str) -> bool:
    available_fonts = fm.get_font_names()
    return font_name in available_fonts


def get_avalible_font_by_names(font_names: list[str], fallback: bool = False) -> str:
    """
    Return the first available font name from a list of font names.

    :param font_names: A list of possible font names.
    :param fallback: Whether to return a fallback font ("DejaVu Sans") if no available font in the list.
    :raises ValueError: If no available font in the list and ``fallback`` is ``False``.
    """
    available_fonts = fm.get_font_names()
    for font_name in font_names:
        if font_name in available_fonts:
            logger.info(f"Found available font: {font_name}")
            return font_name
    if fallback:
        logger.warning(
            f"No available font found in `{font_names=}`. Returning fallback font: DejaVu Sans."
        )
        return "DejaVu Sans"
    else:
        logger.error(f"No available font found in `{font_names=}`.")
        raise ValueError("No available font found.")


def get_recommended_font(style: str) -> str:
    """
    Get the first available font name by specify the font style.

    :param style: One of the "Serif", "Sans", "Mono", "Serif-Hans", or "Sans-Hans".
    """
    font_names = STYLE_TO_RECOMMENDED_FONTS[style]
    return get_avalible_font_by_names(font_names)


if __name__ == "__main__":
    print(fm.get_font_names())
    for i in STYLE_TO_RECOMMENDED_FONTS.keys():
        result = get_recommended_font(style=i)
        print(fm.findfont(result))
