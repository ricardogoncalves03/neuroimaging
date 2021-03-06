from typing import Tuple
from preprocessing.path import Path
import SimpleITK as sitk


class N4Correction(Path):
    """
    Class that implements N4 bias field correction algorithm.
    More info here: https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html
    """
    def __init__(self, img: str, mask: str):
        """
        Initializes a n4 bias field correction object, where `img` is the image to be corrected
        and `mask` is the image mask to help with the correction.
        """
        self.img = img
        self.mask = mask

    def output(self) -> str:
        """Image output"""
        tup = self.__cast(self.img, self.mask)
        img = tup[0]
        mask = tup[1]
        print("Applying N4 Bias Field Correction. This process can take a while")
        n4_img = sitk.N4BiasFieldCorrection(img, mask)
        print("**N4 applied successfully**")
        n4_out = self._output_img(self.img, "n4_")
        sitk.WriteImage(n4_img, n4_out)
        return n4_out

    def __cast(self, read_img: str, read_mask: str) -> Tuple[any, any]:
        """
        Read and cast images to the right format
        """
        if not self.__img_is_nii():
            raise ValueError("The parameters you provided are incorrect. The images must be in a .nii or .nii.gz "
                             "format.")
        # Reading images
        print("Reading and casting {0} and {1}".format(self.img, self.mask))
        read_img = sitk.ReadImage(read_img)
        read_mask = sitk.ReadImage(read_mask)
        # Casting
        if read_img.GetPixelIDTypeAsString() != '32-bit float' and read_img.GetPixelIDTypeAsString() != '64 bit float':
            print("Converting {0} to 32-bit float".format(self.img))
            read_img = sitk.Cast(read_img, sitk.sitkFloat32)
        if read_mask.GetPixelIDTypeAsString() != '8-bit unsigned integer':
            print("Converting {0} to 8-bit unsigned integer".format(self.mask))
            read_mask = sitk.Cast(read_mask, sitk.sitkUInt8)
        return read_img, read_mask

    def __img_is_nii(self) -> bool:
        """Checks if we are providing the right inputs"""
        return self.img.endswith(".nii") and self.img.endswith(".nii.gz") and \
            self.mask.endswith(".nii") or self.mask.endswith(".nii.gz")
