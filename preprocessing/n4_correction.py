from typing import Tuple
from preprocessing.path import Path
import SimpleITK as sitk


class N4Correction(Path):
    """
    Class that implements N4 bias field correction algo to correct low frequency intensity non-uniformity
    present in MRI image data known as a bias or gain field.
    More info here: https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html
    """
    def __init__(self, img: str, mask: str):
        """
        Initializes a n4 bias field correction object, where `img` is the image to be corrected
        and `mask` is the image mask to help with the correction.
        """
        self.img = img
        self.mask = mask

    def output(self) -> sitk.WriteImage:
        """Image output"""
        tup = self.cast(self.img, self.mask)
        img = tup[0]
        mask = tup[1]
        print("Applying N4 Bias Field Correction. This process can take a while")
        n4_img = sitk.N4BiasFieldCorrection(img, mask)
        print("**N4 applied successfully**")
        return sitk.WriteImage(n4_img, self.output_img(self.img, "n4_"))

    def cast(self, read_img, read_mask) -> Tuple[any, any]:
        """
        Read and cast images to the right format
        """
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
