from pathlib import Path


class Directory:
    """Handles directory paths and folder creation for the application."""

    def __init__(self) -> None:
        """Initialize directory paths."""
        self.base_dir = Path(__file__).resolve().parent.parent.parent

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


# Instantiate Directory and create folders
directory = Directory()
directory.create_folders()
