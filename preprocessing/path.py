import os


class Path:
    @staticmethod
    def __get_filename(img_path, prefix="") -> str:
        """Get filename"""
        return prefix + os.path.basename(img_path)

    def _output_img(self, img_path, prefix=""):
        """
        Add a prefix in your output images. They will be placed in the same folder as the original ones
        If no prefix is given, the image will keep the same name as the original.
        """
        return os.path.join(os.path.dirname(img_path), self.__get_filename(img_path, prefix))
