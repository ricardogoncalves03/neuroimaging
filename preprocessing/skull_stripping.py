import subprocess
from typing import Tuple
from preprocessing.path import Path


class SkullStripping(Path):
    """
    Skull stripping using ROBEX tool - https://www.nitrc.org/projects/robex
    """

    def __init__(self, img: str, robex_path: str):
        """
        Initializes a skull stripping object, where `img_path` is the path to the NIfTI image,
        and `robex_path` is the path to the file runROBEX.sh
        """
        self.img = img
        self.robex_path = robex_path

    def start(self) -> Tuple[str, str]:
        """Start skull stripping process"""
        if not (self.img.endswith(".nii") or self.img.endswith(".nii.gz")
                and self.robex_path.endswith("runROBEX.sh")):
            raise ValueError("The parameters you provided are incorrect. The image must be in a .nii or .nii.gz "
                             "format. Also, make sure the ROBEX file is runROBEX.sh")
        ss_img = self._output_img(self.img, "ss_")
        mask_img = self._output_img(self.img, "mask_")
        subprocess.call([self.robex_path, self.img, ss_img, mask_img])
        return ss_img, mask_img
