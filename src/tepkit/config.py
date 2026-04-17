"""
Load Tepkit configuration files.

[zh-CN]
加载并合并 Tepkit 配置文件。
"""

import tomllib
from pathlib import Path


def merge_dict(base: dict, override: dict) -> dict:
    """
    Merge two dictionaries recursively.
    
    [zh-CN]
    递归合并两个字典。
    
    :param base: Base mapping.
    :param override: Override mapping.
    :return: Merged dictionary.
    
    """
    # Copy the input mapping to avoid mutating it.
    # 复制输入映射，避免修改原始值。
    merged_dict = base.copy()
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            # Merge nested mappings recursively.
            # 递归合并嵌套映射。
            merged_dict[key] = merge_dict(merged_dict[key], value)
        else:
            # Replace scalars and non-mapping values.
            # 覆盖标量值或替换非字典条目。
            merged_dict[key] = value
    return merged_dict


class ConfigLoader:
    """
    Load config from package and project TOML files.
    
    [zh-CN]
    从包目录和项目目录的 TOML 文件加载配置数据。
    
    """

    def __init__(self):
        current_file_path = Path(__file__).resolve()
        package_root = current_file_path.parent
        default_config_path = package_root / "tepkit.default.config.toml"
        custom_config_path = package_root / "tepkit.custom.config.toml"
        develop_config_path = package_root / "tepkit.develop.config.toml"
        project_config_path = Path("./tepkit.config.toml").resolve()

        # Load package defaults.
        # 加载包内默认配置。
        with open(default_config_path, "rb") as file:
            default_config = tomllib.load(file)
        config = default_config.copy()

        # Load user overrides when present.
        # 如果存在则加载用户自定义配置。
        if custom_config_path.exists():
            with open(custom_config_path, "rb") as file:
                custom_config = tomllib.load(file)
            config = merge_dict(config, custom_config)
        else:
            # Create an empty custom config file.
            # 创建自定义配置文件占位。
            custom_config_path.touch()

        # Load development overrides when present.
        # 如果存在则加载开发环境覆盖配置。
        if develop_config_path.exists():
            with open(develop_config_path, "rb") as file:
                develop_config = tomllib.load(file)
            config = merge_dict(config, develop_config)

        # Load project overrides when present.
        # 如果存在则加载项目级覆盖配置。
        if project_config_path.exists():
            with open(project_config_path, "rb") as file:
                project_config = tomllib.load(file)
            config = merge_dict(config, project_config)

        self.config = config


def get_config() -> dict:
    """
    Return the merged Tepkit config.
    
    [zh-CN]
    返回合并后的 Tepkit 配置。
    
    :return: Merged config.
    
    """
    config_loader = ConfigLoader()
    config = config_loader.config
    return config


if __name__ == "__main__":
    from rich import print

    print(get_config())