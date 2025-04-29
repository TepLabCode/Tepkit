def get_decimal_formatter(decimal=2):
    def formatter(value, tick_number=None):
        if value < 0:
            return "− " + f"{abs(value):.{decimal}f}"
        else:
            return f"{value:.{decimal}f}"

    return formatter
