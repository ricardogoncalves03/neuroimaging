import os


class Path:
    def get_filename(self, img_path, prefix="") -> str:
        """Get filename"""
        return prefix + os.path.basename(img_path)

    def output_img(self, img_path, prefix=""):
        """
        Add a prefix in your output images. They will be placed in the same folder as the original ones
        If no prefix is given, the image will keep the same name as the original.
        """
        return os.path.join(os.path.dirname(img_path), self.get_filename(img_path, prefix))
