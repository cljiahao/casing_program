import sys
from pathlib import Path


class Directory:
    """Handles directory paths and folder creation for the application."""

    def __init__(self) -> None:
        """Initialize directory paths."""
        self.src_dir = Path(__file__).resolve().parent.parent

        self.base_dir = self.src_dir.parent

        # Log folder
        self.log_dir = self.base_dir / "log"

        # Config folder
        self.config_dir = self.base_dir / "config"

    def create_folders(self) -> None:
        """Create necessary folders for logging, configuration, and data."""
        folders = [
            self.log_dir,
            self.config_dir,
        ]
        for folder in folders:
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {folder}: {e}")

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        base_path = Path(getattr(sys, "_MEIPASS", self.src_dir))
        return base_path / relative_path


# Instantiate Directory and create folders
directory = Directory()
directory.create_folders()
