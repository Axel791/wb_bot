import time
import subprocess

from pathlib import Path
from loguru import logger

from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileModifiedEvent,
    FileDeletedEvent,
)

from app.core.config import settings


class ChangeHandler(FileSystemEventHandler):
    """Handler для отслеживания изменения в боте"""

    def __init__(self, script_name) -> None:
        self.script_name = script_name
        self.process = subprocess.Popen(["python3", self.script_name])

    def on_any_event(self, event):
        if event.is_directory:
            return None

        if "__pycache__" in Path(event.src_path).parts:
            return None

        if isinstance(event, (FileCreatedEvent, FileModifiedEvent, FileDeletedEvent)):
            if settings.debug:
                logger.info(
                    f"Detected change in: {event.src_path}. Change type: {event.event_type}"
                )
            self.restart_script()

    def restart_script(self):
        logger.info("Reloading bot...")
        self.process.kill()
        self.process = subprocess.Popen(["python3", self.script_name])


if __name__ == "__main__":
    app_dir = Path("/app/app")
    script_path = app_dir / "main.py"

    event_handler = ChangeHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, str(app_dir), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
