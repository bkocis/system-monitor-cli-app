"""
Configuration management for System Monitor CLI Dashboard.
"""

import copy
import json
from pathlib import Path
from typing import Any


class Config:
    """Configuration manager for the system monitor."""

    DEFAULT_CONFIG = {
        "refresh_rate": 1.0,  # seconds
        "max_history_points": 100,
        "temperature_thresholds": {
            "warning": 70,  # Celsius
            "critical": 80,  # Celsius
        },
        "display": {
            "show_gpu": True,
            "show_network": False,
            "graph_height": 8,
            "graph_length": 100,
        },
        "colors": {"normal": "green", "warning": "yellow", "critical": "red"},
        "filters": {
            "exclude_virtual_filesystems": True,
            "exclude_loop_devices": True,
            "exclude_snap_mounts": True,
        },
    }

    def __init__(self, config_file: str | None = None):
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            config_dir = Path.home() / ".config" / "system-monitor"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"

        self.config_file = Path(config_file)
        self._config = self.load_config()

    def load_config(self) -> dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = copy.deepcopy(self.DEFAULT_CONFIG)
                    self._deep_update(config, loaded_config)
                    return config
            except (OSError, json.JSONDecodeError) as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
                print("Using default configuration.")

        return copy.deepcopy(self.DEFAULT_CONFIG)

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self._config, f, indent=2)
        except OSError as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'display.show_gpu')."""
        keys = key.split(".")
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def _deep_update(
        self, base_dict: dict[str, Any], update_dict: dict[str, Any]
    ) -> None:
        """Recursively update base_dict with values from update_dict."""
        for key, value in update_dict.items():
            if (
                isinstance(value, dict)
                and key in base_dict
                and isinstance(base_dict[key], dict)
            ):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    @property
    def refresh_rate(self) -> float:
        """Get refresh rate in seconds."""
        return self.get("refresh_rate", 1.0)

    @property
    def max_history_points(self) -> int:
        """Get maximum number of history points to keep."""
        return self.get("max_history_points", 100)

    @property
    def temperature_warning_threshold(self) -> int:
        """Get temperature warning threshold in Celsius."""
        return self.get("temperature_thresholds.warning", 70)

    @property
    def temperature_critical_threshold(self) -> int:
        """Get temperature critical threshold in Celsius."""
        return self.get("temperature_thresholds.critical", 80)


# Global configuration instance
config = Config()
