import os
import SimpleITK as sitk
from preprocessing.path import Path
from colorama import Fore

elastix_image_filter = sitk.ElastixImageFilter()
TEMP_IMG = "r_temp.nii"


class Registration(Path):
    """
    Class to register two NIfTI images, producing a rigid registration which is going to be improved by an
    affine registration order 0. Tool used is SimpleElastix (https://simpleelastix.github.io/)
    """

    def __init__(self, fixed_img: str, moving_img: str):
        """
        Initializes a registration object, where `fixed_img` is the image used as baseline
        and `moving_img` is the image we want to register
        """
        self.fixed_img = fixed_img
        self.moving_img = moving_img

    def start(self) -> None:
        """Start registration process with both rigid and affine"""
        self.rigid_registration()
        self.affine_registration()
        os.remove(TEMP_IMG)  # Remove temporary files
        os.remove("TransformParameters.0.txt")  # Remove unnecessary files

    def rigid_registration(self) -> None:
        """
        Rigid registration.
        """
        if self.is_img_nii():
            elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
            elastix_image_filter.SetMovingImage(sitk.ReadImage(self.moving_img))
            elastix_image_filter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
            elastix_image_filter.Execute()
            sitk.WriteImage(elastix_image_filter.GetResultImage(), TEMP_IMG)
        else:
            print(Fore.RED + "The parameters you provided are incorrect. The images must be in a .nii or .nii.gz "
                             "format.")

    def affine_registration(self) -> None:
        """
        Affine registration. Should be used after the rigid registration to improve results.
        """
        if self.is_img_nii():
            elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
            elastix_image_filter.SetMovingImage(sitk.ReadImage(TEMP_IMG))
            transformation_map = sitk.GetDefaultParameterMap("affine")
            transformation_map['FinalBSplineInterpolationOrder'] = ['0']
            elastix_image_filter.SetParameterMap(transformation_map)
            elastix_image_filter.Execute()
        else:
            print(Fore.RED + "The parameters you provided are incorrect. The images must be in a .nii or .nii.gz "
                             "format.")

    def output(self) -> sitk.WriteImage:
        """Image output"""
        return self.output_img(self.moving_img, "r")

    def remove_files(self) -> None:
        """Delete temporary and unnecessary files"""
        os.remove(TEMP_IMG)
        os.remove("TransformParameters.0.txt")

    def is_img_nii(self) -> bool:
        return self.fixed_img.endswith(".nii") or self.fixed_img.endswith(".nii.gz") and \
               self.moving_img.endswith(".nii") or self.moving_img.endswith(".nii.gz")
