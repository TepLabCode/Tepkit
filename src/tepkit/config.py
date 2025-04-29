from pathlib import Path

import tomllib


def merge_dict(dict1: dict, dict2: dict):
    """
    将 dict2 合并到 dict1 中
    """
    # 创建一个新字典，用于存储合并后的结果
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if (
            key in merged_dict
            and isinstance(merged_dict[key], dict)
            and isinstance(value, dict)
        ):
            # 如果键已经存在，并且值都为词典，则递归合并
            merged_dict[key] = merge_dict(merged_dict[key], value)
        else:
            # 否则，直接赋值
            merged_dict[key] = value
    return merged_dict


class ConfigLoader:
    def __init__(self):
        current_file_path = Path(__file__).resolve()
        package_root = current_file_path.parent
        default_config_path = package_root / "tepkit.default.config.toml"
        custom_config_path = package_root / "tepkit.custom.config.toml"
        develop_config_path = package_root / "tepkit.develop.config.toml"
        project_config_path = Path("./tepkit.config.toml").resolve()
        # 读取默认设置
        with open(default_config_path, "rb") as file:
            default_config = tomllib.load(file)
            self.config = default_config.copy()
        # 读取自定义设置
        if custom_config_path.exists():
            with open(custom_config_path, "rb") as file:
                custom_config = tomllib.load(file)
                self.config = merge_dict(self.config, custom_config)
        else:
            custom_config_path.touch()
        # 读取开发用设置
        if develop_config_path.exists():
            with open(develop_config_path, "rb") as file:
                custom_config = tomllib.load(file)
                self.config = merge_dict(self.config, custom_config)
        # 读取当前路径设置
        if project_config_path.exists():
            with open(project_config_path, "rb") as file:
                custom_config = tomllib.load(file)
                self.config = merge_dict(self.config, custom_config)


def get_config():
    config_loader = ConfigLoader()
    config = config_loader.config
    return config
