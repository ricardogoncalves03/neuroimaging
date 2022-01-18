import os
import SimpleITK as sitk
from preprocessing.path import Path
import subprocess
from typing import Tuple
import numpy as np
import nibabel as nib
from numpy import ndarray
from numpy.ma import MaskedArray
from skimage.measure import label, regionprops


class Registration(Path):
    """
    Class to register two NIfTI images, producing a rigid registration which is going to be improved by an
    affine registration order 0. Tool used is SimpleElastix (https://simpleelastix.github.io/)
    """
    __TEMP_IMG = "r_temp.nii"
    __elastix_image_filter = sitk.ElastixImageFilter()

    def __init__(self, fixed_img: str, moving_img: str):
        """
        Initializes a registration object, where `fixed_img` is the image used as baseline
        and `moving_img` is the image we want to register
        """
        self.fixed_img = fixed_img
        self.moving_img = moving_img

    def start(self) -> None:
        """Start registration process with both rigid and affine"""
        self.__rigid_registration()
        self.__affine_registration()
        self.__remove_files()

    def output(self) -> str:
        """Image output"""
        return self._output_img(self.moving_img, "r")

    def __rigid_registration(self) -> None:
        """
        Rigid registration.
        """
        if not self.__img_is_nii():
            raise ValueError("The parameters you provided are incorrect. The images must be in a .nii or .nii.gz "
                             "format.")
        Registration.__elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        Registration.__elastix_image_filter.SetMovingImage(sitk.ReadImage(self.moving_img))
        Registration.__elastix_image_filter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
        Registration.__elastix_image_filter.Execute()
        sitk.WriteImage(Registration.__elastix_image_filter.GetResultImage(), Registration.__TEMP_IMG)

    def __affine_registration(self) -> None:
        """
        Affine registration. Must be used after the rigid registration to improve results.
        """
        Registration.__elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        Registration.__elastix_image_filter.SetMovingImage(sitk.ReadImage(Registration.__TEMP_IMG))
        transformation_map = sitk.GetDefaultParameterMap("affine")
        transformation_map['FinalBSplineInterpolationOrder'] = ['0']
        Registration.__elastix_image_filter.SetParameterMap(transformation_map)
        Registration.__elastix_image_filter.Execute()
        img_out = self._output_img(self.moving_img, "r")
        sitk.WriteImage(Registration.__elastix_image_filter.GetResultImage(), img_out)

    @staticmethod
    def __remove_files() -> None:
        """Delete temporary and unnecessary files"""
        os.remove(Registration.__TEMP_IMG)
        os.remove("TransformParameters.0.txt")

    def __img_is_nii(self) -> bool:
        return self.fixed_img.endswith(".nii") or self.fixed_img.endswith(".nii.gz") and \
               self.moving_img.endswith(".nii") or self.moving_img.endswith(".nii.gz")


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

    def output(self) -> Tuple[str, str]:
        """Start skull stripping process"""
        if not self.__nii_and_robex():
            raise ValueError("The parameters you provided are incorrect. The image must be in a .nii or .nii.gz "
                             "format. Also, make sure the ROBEX file is runROBEX.sh")
        ss_img = self._output_img(self.img, "ss_")
        mask_img = self._output_img(self.img, "mask_")
        subprocess.call([self.robex_path, self.img, ss_img, mask_img])
        return ss_img, mask_img

    def __nii_and_robex(self) -> bool:
        """Checks if we are providing the right inputs"""
        return self.img.endswith(".nii") or self.img.endswith(".nii.gz") and \
            self.robex_path.endswith("runROBEX.sh")


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
        self.__masked_nii()

    def output(self) -> str:
        """Normalized img output"""
        self.__nii_matrix[:, :, :] = self.__masked_nii()
        norm_out = self._output_img(self.img, "norm_")
        self.__nii.to_filename(norm_out)  # saving resulting nifti
        print("Cheers! {0} is now normalized".format(self.img))
        return norm_out

    def __load_nii(self) -> ndarray:
        """Make a copy of `nii_matrix`, to safely work on nii_copy matrix"""
        print("{0}loaded. Making a copy of its matrix".format(self.img))
        nii_copy = np.copy(self.__nii_matrix)
        print("Copy created")
        return nii_copy

    def __masked_nii(self) -> MaskedArray:
        """Normalization process"""
        print("Starting normalization process")
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
        print("Normalization process finished")
        return masked_nii

    def __img_is_nii(self) -> bool:
        """Checks if we are providing the right input"""
        return self.img.endswith(".nii") or self.img.endswith(".nii.gz")
