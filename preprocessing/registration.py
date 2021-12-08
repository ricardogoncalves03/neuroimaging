import os
import SimpleITK as sitk
from preprocessing.path import Path


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
        self._affine_registration()
        self.__remove_files()

    def output(self) -> any:
        """Image output"""
        return self._output_img(self.moving_img, "r")

    def __rigid_registration(self) -> None:
        """
        Rigid registration.
        """
        if not self.__is_img_nii():
            raise ValueError("The parameters you provided are incorrect. The images must be in a .nii or .nii.gz "
                             "format.")
        Registration.__elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        Registration.__elastix_image_filter.SetMovingImage(sitk.ReadImage(self.moving_img))
        Registration.__elastix_image_filter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
        Registration.__elastix_image_filter.Execute()
        sitk.WriteImage(Registration.__elastix_image_filter.GetResultImage(), Registration.__TEMP_IMG)

    def _affine_registration(self) -> None:
        """
        Affine registration. Must be used after the rigid registration to improve results.
        """
        Registration.__elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        Registration.__elastix_image_filter.SetMovingImage(sitk.ReadImage(Registration.__TEMP_IMG))
        transformation_map = sitk.GetDefaultParameterMap("affine")
        transformation_map['FinalBSplineInterpolationOrder'] = ['0']
        Registration.__elastix_image_filter.SetParameterMap(transformation_map)
        Registration.__elastix_image_filter.Execute()

    @staticmethod
    def __remove_files() -> None:
        """Delete temporary and unnecessary files"""
        os.remove(Registration.__TEMP_IMG)
        os.remove("TransformParameters.0.txt")

    def __is_img_nii(self) -> bool:
        return self.fixed_img.endswith(".nii") or self.fixed_img.endswith(".nii.gz") and \
               self.moving_img.endswith(".nii") or self.moving_img.endswith(".nii.gz")
