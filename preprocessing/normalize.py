import numpy as np
import nibabel as nib
from numpy import ndarray
from numpy.ma import MaskedArray
from skimage.measure import label, regionprops

from preprocessing.path import Path


class Normalize(Path):
    """Class to normalize NIfTI images according to Qtim deep learning tutorial.
     Results will have 0 mean, min intensity of around -2 and max intensity of around 2
     """

    def __init__(self, img: str):
        """
        Initializes a normalization object, where `img` is the img to be normalized,
        `nii` is the image loaded using nibabel, so it can be manipulated and `nii_matrix`
        is the image matrix info
        """
        self.img = img

    def _start(self):
        nii = nib.load(self.img)
        nii_matrix = nii.get_data()
        nii_copy = np.copy(nii_matrix)

        label_image = label(nii_copy)
        largest_label, largest_area = None, 0
        for region in regionprops(label_image):
            if region.area > largest_area:
                largest_area = region.area
                largest_label = region.label

        mask = label_image == largest_label
        masked_nii = np.ma.masked_where(mask, nii_copy)
        masked_nii = masked_nii - np.mean(masked_nii)
        masked_nii = masked_nii / np.std(masked_nii)
        masked_nii = np.ma.getdata(masked_nii)

        nii_matrix[:, :, :] = masked_nii

        nii.to_filename(self._output_img(self.img, "norm_"))
