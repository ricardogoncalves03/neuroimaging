import os
import SimpleITK as sitk
from preprocessing.path import Path

elastix_image_filter = sitk.ElastixImageFilter()


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

    def rigid_registration(self) -> None:
        elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        elastix_image_filter.SetMovingImage(sitk.ReadImage(self.moving_img))
        elastix_image_filter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
        elastix_image_filter.Execute()
        sitk.WriteImage(elastix_image_filter.GetResultImage(), "r_temp.nii")

    def affine_registration(self) -> None:
        elastix_image_filter.SetFixedImage(sitk.ReadImage(self.fixed_img))
        elastix_image_filter.SetMovingImage(sitk.ReadImage("r_temp.nii"))
        transformation_map = sitk.GetDefaultParameterMap("affine")
        transformation_map['FinalBSplineInterpolationOrder'] = ['0']
        elastix_image_filter.SetParameterMap(transformation_map)
        elastix_image_filter.Execute()

    def output(self):
        """Image output"""
        moving_img = self.output(self.moving_img, "r")
        return sitk.WriteImage(elastix_image_filter.GetResultImage(), moving_img)

    def remove_files(self) -> None:
        """Delete temporary and unnecessary files"""
        os.remove("r_temp.nii")
        os.remove("TransformParameters.0.txt")
