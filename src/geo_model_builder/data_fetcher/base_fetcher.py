"""_summary_
"""
import shutil


from pathlib import Path
from abc import ABC, abstractmethod

class BaseDataFetcher(ABC):
    """Base class for data fetchers with common functionality."""
    
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir).absolute()
        self._setup_cache_dir()
    
    def _setup_cache_dir(self):
        """Setup and clean cache directory."""
        if self.cache_dir.exists():
            try:
                for item in self.cache_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print("Cleared existing cache directory")
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not clear cache directory: {e}")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def fetch_data(self):
        """Fetch data method to be implemented by child classes."""
        pass