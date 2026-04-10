from __future__ import annotations

import random
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
}


class PhotoRepository:
    def __init__(self, photos_dir: str | Path) -> None:
        self.photos_dir = Path(photos_dir)

    def ensure_exists(self) -> None:
        """Ensure the photo directory exists."""
        self.photos_dir.mkdir(parents=True, exist_ok=True)

    def list_photos(self, shuffle: bool = False) -> list[Path]:
        """
        Return a list of photo paths found in the photos directory.

        By default, files are sorted alphabetically.
        If shuffle=True, the returned list is randomized.
        """
        photos = [
            path
            for path in self.photos_dir.iterdir()
            if path.is_file() and self._is_supported_image(path)
        ]

        photos.sort(key=lambda p: p.name.lower())

        if shuffle:
            random.shuffle(photos)

        return photos

    def count_photos(self) -> int:
        """Return the number of valid photos in the directory."""
        return len(self.list_photos(shuffle=False))

    def has_photos(self) -> bool:
        """Return True if at least one valid photo exists."""
        return self.count_photos() > 0

    def get_photo_paths_as_strings(self, shuffle: bool = False) -> list[str]:
        """Return photo paths as strings, useful for UI/toolkit integration."""
        return [str(path) for path in self.list_photos(shuffle=shuffle)]

    def rescan(self, shuffle: bool = False) -> list[Path]:
        """
        Explicit alias for list_photos(), useful when called from UI logic.
        """
        return self.list_photos(shuffle=shuffle)

    def _is_supported_image(self, path: Path) -> bool:
        """Return True if the file extension is supported."""
        return path.suffix.lower() in SUPPORTED_EXTENSIONS
