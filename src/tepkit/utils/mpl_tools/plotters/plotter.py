def update_config(dict1: dict, dict2: dict):
    """
    Merge dict2 into dict1. All keys in dict2 must exist in dict1.
    If the corresponding values are both dictionaries, merge them recursively.
    """
    # Create a copy of dict1 to avoid modifying it
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        # Raise an error if dict2 contains a key not in dict1
        if key not in merged_dict:
            raise KeyError(f"Key `{key}` not found.")
        if isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = update_config(merged_dict[key], value)
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

    def update_config(self, config: dict):
        self.config = update_config(self.config, config)


class Plotter(BasePlotter):
    pass
