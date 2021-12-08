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
        is the image matrix info
        """
        self.img = img
        if not self.__img_is_nii():
            raise ValueError("The parameter you provided is incorrect. The image must be in a .nii or .nii.gz "
                             "format.")
        self.__nii = nib.load(self.img)
        self.__nii_matrix = self.__nii.get_data()

    def start(self) -> None:
        """Start loading nii and masking it"""
        self.__load_nii()
        print(self.__masked_nii())

    def output(self) -> str:
        """Normalized img output"""
        self.__nii_matrix[:, :, :] = self.__masked_nii()
        norm_out = self._output_img(self.img, "norm_")
        self.__nii.to_filename(norm_out)  # saving resulting nifti
        return norm_out

    def __load_nii(self) -> ndarray:
        """Make a copy of `nii_matrix`, to safely work on nii_copy matrix"""
        nii_copy = np.copy(self.__nii_matrix)
        print("creating a copy")
        return nii_copy

    def __masked_nii(self) -> MaskedArray:
        """Normalization process"""
        print(self.__load_nii())
        label_image = label(self.__load_nii() == 0)
        largest_label, largest_area = None, 0
        for region in regionprops(label_image):
            if region.area > largest_area:
                largest_area = region.area
                largest_label = region.label
        mask = label_image == largest_label
        masked_nii = np.ma.masked_where(mask, self.__load_nii())
        masked_nii = masked_nii - np.mean(masked_nii)
        masked_nii = masked_nii / np.std(masked_nii)
        masked_nii = np.ma.getdata(masked_nii)
        return masked_nii

    def __img_is_nii(self) -> bool:
        """Checks if we are providing the right input"""
        return self.img.endswith(".nii") or self.img.endswith(".nii.gz")
