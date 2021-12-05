import subprocess
from preprocessing.path import Path
from colorama import Fore


class SkullStripping(Path):
    """
    Skull stripping using ROBEX tool - https://www.nitrc.org/projects/robex
    """
    def __init__(self, img_path: str, robex_path: str):
        """
        Initializes a skull stripping object, where `img_path` is the path to the NIfTI image,
        and `robex_path` is the path to the file runROBEX.sh
        """
        self.img_path = img_path
        self.robex_path = robex_path

    def start(self) -> None:
        """Start skull stripping process"""
        if self.img_path.endswith(".nii") or self.img_path.endswith(".nii.gz") \
                and self.robex_path.endswith("runROBEX.sh"):
            ss_img = self.output(self.img_path, "ss_")
            print(ss_img)
            mask_img = self.output(self.img_path, "mask_")
            print(mask_img)
            subprocess.call([self.robex_path, self.img_path, ss_img, mask_img])
        else:
            print(Fore.RED + "The parameters you provided are incorrect. The image must be in a .nii or .nii.gz "
                             "format. Also, make sure the ROBEX file is runROBEX.sh")
