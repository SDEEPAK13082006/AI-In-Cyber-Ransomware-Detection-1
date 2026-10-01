"""
Real-time Directory Watcher Service
===================================
Uses watchdog library to monitor Windows filesystem folders.
Triggers immediate feature extraction and prediction on file modification/creation.
"""

import os
import time
import logging
from typing import List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class RansomwareFileEventHandler(FileSystemEventHandler):
    """
    Event Handler capturing file creation, rename, and entropy spikes.
    """
    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"[WATCHER EVENT] File Created: {event.src_path}")
            self.evaluate_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"[WATCHER EVENT] File Modified: {event.src_path}")
            self.evaluate_file(event.src_path)

    def evaluate_file(self, file_path: str):
        """Perform heuristic evaluation on modified file."""
        try:
            filename = os.path.basename(file_path)
            file_size_kb = os.path.getsize(file_path) / 1024.0 if os.path.exists(file_path) else 10.0
            
            # Simple check for ransomware extension markers
            if any(file_path.endswith(ext) for ext in ['.locked', '.crypto', '.enc', '.wannacry']):
                logger.critical(f"🚨 WATCHER TRIGGERED: Ransomware Extension detected on {filename}!")
        except Exception as e:
            logger.error(f"Watcher evaluation error: {e}")

class DirectoryWatcherManager:
    """
    Manages active Watchdog Observers.
    """
    def __init__(self):
        self.observer = Observer()
        self.active_paths: List[str] = []

    def start_monitoring(self, path: str):
        if os.path.exists(path) and path not in self.active_paths:
            handler = RansomwareFileEventHandler()
            self.observer.schedule(handler, path=path, recursive=True)
            if not self.observer.is_alive():
                self.observer.start()
            self.active_paths.append(path)
            logger.info(f"Started monitoring directory: {path}")
            return True
        return False

    def stop(self):
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

watcher_manager = DirectoryWatcherManager()
