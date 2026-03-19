"""配置管理基础类

提供统一的配置管理，配置文件存储在 ~/.dong/config.json

所有咚咚家族 CLI 共享一个配置文件，按 CLI 名称分 section。
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

# 统一配置文件
DONG_DIR = Path.home() / ".dong"
CONFIG_FILE = DONG_DIR / "config.json"


class Config:
    """
    配置管理基类

    子类需要实现：
    - get_name(): 返回 CLI 名称
    - get_defaults(): 返回默认配置字典

    配置文件格式:
    {
        "log": {"default_group": "work", ...},
        "cang": {"default_account": 1, ...},
        ...
    }
    """

    _all_config: Optional[Dict[str, Any]] = None

    @classmethod
    def get_name(cls) -> str:
        """返回 CLI 名称（子类必须实现）"""
        raise NotImplementedError

    @classmethod
    def get_defaults(cls) -> Dict[str, Any]:
        """返回默认配置（子类必须实现）"""
        raise NotImplementedError

    @classmethod
    def get_config_file(cls) -> Path:
        """获取统一配置文件路径"""
        return CONFIG_FILE

    @classmethod
    def _load_all(cls) -> Dict[str, Any]:
        """加载整个配置文件"""
        if cls._all_config is not None:
            return cls._all_config

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    cls._all_config = json.load(f)
            except (json.JSONDecodeError, IOError):
                cls._all_config = {}
        else:
            cls._all_config = {}

        return cls._all_config

    @classmethod
    def _save_all(cls, config: Dict[str, Any]) -> None:
        """保存整个配置文件"""
        DONG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        cls._all_config = config

    @classmethod
    def load(cls) -> Dict[str, Any]:
        """加载当前 CLI 的配置"""
        all_config = cls._load_all()
        name = cls.get_name()
        defaults = cls.get_defaults()

        if name not in all_config:
            # 初始化该 CLI 的配置为默认值
            all_config[name] = defaults
            cls._save_all(all_config)

        # 合并默认配置
        return {**defaults, **all_config.get(name, {})}

    @classmethod
    def save(cls, config: Dict[str, Any]) -> None:
        """保存当前 CLI 的配置"""
        all_config = cls._load_all()
        name = cls.get_name()
        all_config[name] = config
        cls._save_all(all_config)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置项"""
        config = cls.load()
        return config.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """设置配置项"""
        config = cls.load()
        config[key] = value
        cls.save(config)

    @classmethod
    def reset(cls) -> None:
        """重置当前 CLI 的配置到默认值"""
        all_config = cls._load_all()
        name = cls.get_name()
        if name in all_config:
            del all_config[name]
            cls._save_all(all_config)
        cls._all_config = None
