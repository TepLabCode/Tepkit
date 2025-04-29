def update_config(dict1: dict, dict2: dict):
    """
    将 dict2 合并到 dict1 中
    """
    # 创建一个新字典，用于存储合并后的结果
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key not in merged_dict:
            raise KeyError(f"Key `{key}` not found.")
        else:
            if isinstance(merged_dict[key], dict) and isinstance(value, dict):
                # 如果键已经存在，并且值都为词典，则递归合并
                merged_dict[key] = update_config(merged_dict[key], value)
            else:
                merged_dict[key] = value
    return merged_dict


class Plotter:
    def __init__(self):
        self.config: dict = {}

    def update_config(self, config: dict):
        self.config = update_config(self.config, config)
