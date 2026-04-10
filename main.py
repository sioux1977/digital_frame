from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from config_manager import ConfigManager, ConfigError
from photo_repository import PhotoRepository
from calendar_repository import CalendarRepository
from widgets.slideshow_widget import SlideshowWidget


CONFIG_DIR = Path("/var/lib/digital-frame/config")
PHOTOS_DIR = Path("/var/lib/digital-frame/photos")
EVENTS_FILE = Path("/var/lib/digital-frame/calendar/events.json")


class DigitalFrameRoot(FloatLayout):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.config_manager = ConfigManager(CONFIG_DIR)
        self.photo_repository = PhotoRepository(PHOTOS_DIR)
        self.calendar_repository = CalendarRepository(EVENTS_FILE)

        self._load_initial_state()

        self.slideshow_widget = SlideshowWidget(
            photo_paths=self.photo_paths,
            photo_duration=self.photo_duration,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self.add_widget(self.slideshow_widget)

        self.clock_label = Label(
            text="",
            size_hint=(None, None),
            size=(dp(320), dp(80)),
            pos_hint={"right": 0.98, "top": 0.98},
            halign="right",
            valign="middle",
            font_size="28sp",
            color=(1, 1, 1, 1),
        )
        self.clock_label.bind(size=self._sync_text_size)
        self.add_widget(self.clock_label)

        self.calendar_box = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint=(None, None),
            size=(dp(460), dp(260)),
            pos_hint={"x": 0.02, "top": 0.98},
        )
        self.add_widget(self.calendar_box)

        self._rebuild_calendar_overlay()
        self._update_clock()

        self.slideshow_widget.start()

        Clock.schedule_interval(self._update_clock, 1)
        Clock.schedule_interval(self._refresh_photos_from_disk, 30)
        Clock.schedule_interval(self._refresh_calendar_from_disk, 60)

    def _load_initial_state(self) -> None:
        self.config_manager.ensure_exists()
        self.photo_repository.ensure_exists()
        self.calendar_repository.ensure_exists()

        try:
            self.settings = self.config_manager.load()
        except ConfigError:
            self.config_manager.reset_to_defaults()
            self.settings = self.config_manager.get_all()

        self.photo_duration = float(
            self.config_manager.get("slideshow.photo_duration", 20)
        )
        self.shuffle_enabled = bool(
            self.config_manager.get("slideshow.shuffle", True)
        )
        self.clock_enabled = bool(
            self.config_manager.get("overlay.clock_enabled", True)
        )
        self.calendar_enabled = bool(
            self.config_manager.get("overlay.calendar_enabled", True)
        )
        self.calendar_max_events = int(
            self.config_manager.get("overlay.calendar_max_events", 5)
        )

        self.photo_paths = self.photo_repository.get_photo_paths_as_strings(
            shuffle=self.shuffle_enabled
        )
        self.calendar_events = self.calendar_repository.get_events(
            max_events=self.calendar_max_events
        )

    def _update_clock(self, *_args: Any) -> None:
        if not self.clock_enabled:
            self.clock_label.text = ""
            self.clock_label.opacity = 0
            return

        now = datetime.now()
        self.clock_label.text = now.strftime("%d/%m/%Y\n%H:%M:%S")
        self.clock_label.opacity = 1

    def _refresh_photos_from_disk(self, *_args: Any) -> None:
        new_photo_paths = self.photo_repository.get_photo_paths_as_strings(
            shuffle=self.shuffle_enabled
        )

        if new_photo_paths != self.photo_paths:
            self.photo_paths = new_photo_paths
            self.slideshow_widget.set_photos(self.photo_paths, restart=True)

    def _refresh_calendar_from_disk(self, *_args: Any) -> None:
        self.calendar_events = self.calendar_repository.get_events(
            max_events=self.calendar_max_events
        )
        self._rebuild_calendar_overlay()

    def _rebuild_calendar_overlay(self) -> None:
        self.calendar_box.clear_widgets()

        if not self.calendar_enabled:
            self.calendar_box.opacity = 0
            return

        self.calendar_box.opacity = 1

        title_label = Label(
            text="Upcoming events",
            size_hint=(1, None),
            height=dp(36),
            halign="left",
            valign="middle",
            font_size="22sp",
            bold=True,
            color=(1, 1, 1, 1),
        )
        title_label.bind(size=self._sync_text_size)
        self.calendar_box.add_widget(title_label)

        if not self.calendar_events:
            empty_label = Label(
                text="No upcoming events",
                size_hint=(1, None),
                height=dp(32),
                halign="left",
                valign="middle",
                font_size="18sp",
                color=(1, 1, 1, 1),
            )
            empty_label.bind(size=self._sync_text_size)
            self.calendar_box.add_widget(empty_label)
            return

        for event in self.calendar_events:
            event_text = self._format_event_text(event)

            event_label = Label(
                text=event_text,
                size_hint=(1, None),
                height=dp(44),
                halign="left",
                valign="middle",
                font_size="18sp",
                color=(1, 1, 1, 1),
            )
            event_label.bind(size=self._sync_text_size)
            self.calendar_box.add_widget(event_label)

    def _format_event_text(self, event: dict[str, Any]) -> str:
        date_text = event.get("display_date", "")
        time_text = event.get("display_time", "")
        title = event.get("title", "")
        location = event.get("location", "")

        base = f"{date_text}  {time_text}\n{title}"

        if location:
            base += f" ({location})"

        return base

    @staticmethod
    def _sync_text_size(instance: Label, size: tuple[float, float]) -> None:
        instance.text_size = size


class DigitalFrameApp(App):
    def build(self) -> DigitalFrameRoot:
        Window.clearcolor = (0, 0, 0, 1)
        return DigitalFrameRoot()


if __name__ == "__main__":
    DigitalFrameApp().run()
