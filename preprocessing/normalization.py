import numpy as np
import nibabel as nib
from numpy import ndarray
from numpy.ma import MaskedArray
from skimage.measure import label, regionprops

from preprocessing.path import Path


class Normalization(Path):
    """Class to normalize NIfTI images according to Qtim deep learning tutorial.
     Results will have 0 mean, min intensity of around -2 and max intensity of around 2
     """

    def __init__(self, img: str):
        """
        Initializes a normalization object, where `img` is the img to be normalized,
        `nii` is the image loaded using nibabel, so it can be manipulated and `nii_matrix`
        is the image natrix info
        """
        self.img = img
        self.nii = nib.load(self.img)
        self.nii_matrix = self.nii.get_data()

    def start(self) -> None:
        """Start loading nii and masking it"""
        self.load_nii()
        a = self.masked_nii()

        self.nii_matrix[:, :, :] = a
        return self.nii.to_filename(self.output_img(self.img, "norm_"))

    def output(self) -> any:
        """Normalized img output"""
        self.nii_matrix[:, :, :] = self.masked_nii()
        return self.nii.to_filename(self.output_img(self.img, "norm_"))  # saving resulting nifti

    def load_nii(self) -> ndarray:
        """Make a copy of `nii_matrix`, to safely work in nii_copy matrix"""
        nii_copy = np.copy(self.nii_matrix)
        print("load_nii")
        return nii_copy

    def masked_nii(self) -> MaskedArray:
        """To be commented"""
        label_image = label(self.load_nii() == 0)
        largest_label, largest_area = None, 0
        for region in regionprops(label_image):
            if region.area > largest_area:
                largest_area = region.area
                largest_label = region.label

        mask = label_image == largest_label
        masked_nii = np.ma.masked_where(mask, self.load_nii())
        masked_nii = masked_nii - np.mean(masked_nii)
        masked_nii = masked_nii / np.std(masked_nii)
        masked_nii = np.ma.getdata(masked_nii)
        print("masked_nii")
        return masked_nii
