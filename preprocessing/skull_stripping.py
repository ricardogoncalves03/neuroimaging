import os.path
import subprocess


class SkullStripping:
    """
    Skull stripping with ROBEX tool - https://www.nitrc.org/projects/robex.
    Output: ss_img.nii, mask_img.nii
    """

    def __init__(self, img_path: str, robex_path: str):
        self.img_path = img_path
        """Path to the NIfTI image"""
        self.robex_path = robex_path
        """Path to the file runROBEX.sh"""

    def start(self) -> None:
        """Start skull stripping process"""
        path_name: str = os.path.dirname(self.img_path)  # Get path without the filename
        img_name: str = os.path.basename(self.img_path)  # Extract filename from the path
        img_out: str = "ss_" + img_name
        img_path: str = os.path.join(path_name, img_out)
        img_mask_out: str = "mask_" + img_name
        img_mask_path: str = os.path.join(path_name, img_mask_out)
        subprocess.call([self.robex_path, self.img_path, img_path, img_mask_path])

# Use try except to only accept as input nii file and ROBEX.sh
