from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS: dict[str, Any] = {
    "slideshow": {
        "photo_duration": 20,
        "fade_enabled": True,
        "fade_duration": 1.0,
        "animation_enabled": True,
        "zoom_percent": 8,
        "pan_x_px": 30,
        "pan_y_px": 15,
        "shuffle": True,
    },
    "overlay": {
        "clock_enabled": True,
        "calendar_enabled": True,
        "calendar_max_events": 5,
    },
    "ui": {
        "show_settings_button": True,
    },
}


class ConfigError(Exception):
    """Generic configuration error."""


class ConfigManager:
    def __init__(self, config_dir: str | Path) -> None:
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "settings.json"
        self._settings: dict[str, Any] = {}

    def ensure_exists(self) -> None:
        """
        Ensure config directory and settings file exist.
        If the file does not exist, create it with default settings.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self._settings = deepcopy(DEFAULT_SETTINGS)
            self.save()
        else:
            self.load()

    def load(self) -> dict[str, Any]:
        """
        Load settings from disk.
        If the file is invalid, raise ConfigError.
        Missing keys are filled with defaults.
        """
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found: {self.config_file}")
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON in configuration file: {exc}") from exc
        except OSError as exc:
            raise ConfigError(f"Unable to read configuration file: {exc}") from exc

        if not isinstance(data, dict):
            raise ConfigError("Configuration root must be a JSON object")

        self._settings = self._merge_with_defaults(data)
        return self._settings

    def save(self) -> None:
        """Save current settings to disk."""
        try:
            with self.config_file.open("w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
                f.write("\n")
        except OSError as exc:
            raise ConfigError(f"Unable to write configuration file: {exc}") from exc

    def get_all(self) -> dict[str, Any]:
        """Return a deep copy of the full settings dictionary."""
        return deepcopy(self._settings)

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a config value using dot notation, e.g.:
            get("slideshow.fade_duration")
        """
        parts = path.split(".")
        current: Any = self._settings

        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]

        return current

    def set(self, path: str, value: Any, autosave: bool = True) -> None:
        """
        Set a config value using dot notation, e.g.:
            set("slideshow.fade_duration", 1.5)
        """
        parts = path.split(".")
        current = self._settings

        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

        if autosave:
            self.save()

    def reset_to_defaults(self, autosave: bool = True) -> None:
        """Reset all settings to defaults."""
        self._settings = deepcopy(DEFAULT_SETTINGS)
        if autosave:
            self.save()

    def update(self, new_settings: dict[str, Any], autosave: bool = True) -> None:
        """
        Merge a partial settings dictionary into the current config.
        """
        self._settings = self._deep_merge(self._settings, new_settings)
        self._settings = self._merge_with_defaults(self._settings)

        if autosave:
            self.save()

    def _merge_with_defaults(self, user_settings: dict[str, Any]) -> dict[str, Any]:
        """
        Merge user settings on top of defaults, preserving missing keys.
        """
        return self._deep_merge(deepcopy(DEFAULT_SETTINGS), user_settings)

    def _deep_merge(self, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """
        Recursively merge override into base.
        """
        for key, value in override.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
