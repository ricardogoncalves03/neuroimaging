import os


class Path:
    """Class responsible for extracting the filename and path"""

    @staticmethod
    def get_filename(img_path: str) -> str:
        """Extract filename from a path"""
        return os.path.basename(img_path)

    @staticmethod
    def _path(img_path: str) -> str:
        """Get path without filename"""
        return os.path.dirname(img_path)
