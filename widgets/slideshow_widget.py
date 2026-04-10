from __future__ import annotations

from pathlib import Path
from typing import Sequence

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class SlideshowWidget(FloatLayout):
    photo_duration = NumericProperty(20.0)
    current_photo_path = StringProperty("")

    def __init__(
        self,
        photo_paths: Sequence[str | Path] | None = None,
        photo_duration: float = 20.0,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.photo_duration = max(1.0, float(photo_duration))
        self.photo_paths: list[str] = [str(path) for path in (photo_paths or [])]
        self.current_index: int = 0
        self._slideshow_event = None

        self.image_widget = Image(
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )

        self.empty_label = Label(
            text="No photos available",
            font_size="24sp",
            halign="center",
            valign="middle",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self.empty_label.bind(size=self._update_empty_label_text_size)

        self.add_widget(self.image_widget)
        self.add_widget(self.empty_label)

        self._refresh_view()

    def start(self) -> None:
        """Start automatic slideshow rotation."""
        self.stop()

        if len(self.photo_paths) <= 1:
            return

        self._slideshow_event = Clock.schedule_interval(
            self._show_next_photo,
            self.photo_duration,
        )

    def stop(self) -> None:
        """Stop automatic slideshow rotation."""
        if self._slideshow_event is not None:
            self._slideshow_event.cancel()
            self._slideshow_event = None

    def set_photos(self, photo_paths: Sequence[str | Path], restart: bool = True) -> None:
        """
        Replace the current photo list.
        """
        self.photo_paths = [str(path) for path in photo_paths]
        self.current_index = 0
        self._refresh_view()

        if restart:
            self.start()

    def set_photo_duration(self, seconds: float, restart: bool = True) -> None:
        """
        Update slideshow interval duration.
        """
        self.photo_duration = max(1.0, float(seconds))

        if restart:
            self.start()

    def show_next_photo(self) -> None:
        """Public helper to move to the next photo."""
        self._show_next_photo()

    def show_previous_photo(self) -> None:
        """Move to the previous photo."""
        if not self.photo_paths:
            self._refresh_view()
            return

        self.current_index = (self.current_index - 1) % len(self.photo_paths)
        self._refresh_view()

    def _show_next_photo(self, *_args) -> None:
        if not self.photo_paths:
            self._refresh_view()
            return

        self.current_index = (self.current_index + 1) % len(self.photo_paths)
        self._refresh_view()

    def _refresh_view(self) -> None:
        """Refresh the currently displayed photo or fallback message."""
        if not self.photo_paths:
            self.current_photo_path = ""
            self.image_widget.opacity = 0
            self.image_widget.source = ""
            self.empty_label.opacity = 1
            return

        if self.current_index >= len(self.photo_paths):
            self.current_index = 0

        self.current_photo_path = self.photo_paths[self.current_index]
        self.image_widget.source = self.current_photo_path
        self.image_widget.reload()
        self.image_widget.opacity = 1
        self.empty_label.opacity = 0

    def _update_empty_label_text_size(self, instance: Label, size: tuple[float, float]) -> None:
        instance.text_size = size
