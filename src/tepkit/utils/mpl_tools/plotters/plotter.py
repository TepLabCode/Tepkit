from matplotlib import pyplot as plt


def update_config(
    dict1: dict,
    dict2: dict,
    mode: str = "normal",
):
    """
    Merge dict2 into dict1.
    If the corresponding values are both dictionaries, merge them recursively.
    """
    # Create a copy of dict1 to avoid modifying it
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key not in merged_dict:
            match mode:
                case "strict":
                    raise KeyError(f"Key `{key}` not found in base dict.")
                case "free":
                    merged_dict[key] = value
                case "normal":
                    if key.endswith("kwargs"):
                        merged_dict[key] = value
                    else:
                        raise KeyError(f"Key `{key}` not found in base dict.")
                case _:
                    raise ValueError(f"Invalid mode `{mode}`.")
        elif isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = update_config(merged_dict[key], value, mode=mode)
        else:
            # Otherwise, simply update the value
            merged_dict[key] = value
    return merged_dict


class BasePlotter:
    def __init__(self):
        self.config: dict = {}

    def get_config(self) -> dict:
        """
        Can be overridden to provide custom configuration for the plotter.
        """
        return self.config.copy()

    def update_config(self, config: dict, mode: str = "normal"):
        self.config = update_config(self.config, config, mode=mode)

    def save(self, save_path: str, dpi=300):
        plt.savefig(save_path, dpi=dpi)

    def close(self):
        plt.close()


class Plotter(BasePlotter):
    pass
