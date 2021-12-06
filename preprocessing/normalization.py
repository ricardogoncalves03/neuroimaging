import numpy as np
import nibabel as nib
from skimage.measure import label, regionprops

from preprocessing.path import Path


class Normalization(Path):
    """Class to normalize NIfTI images according to Qtim deep learning tutorial.
     Results will have 0 mean, min intensity of around -2 and max intensity of around 2
     """
    def __init__(self, img: str):
        self.img = img

    def nii(self):
        nii = nib.load(self.img) # load nii image
        nii_matrix = nii.get_data() # load nii matrix
        nii_copy = np.copy(nii_matrix)

        label_image = label(nii_copy == 0)

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

        nii.to_filename(final_nii)  # saving resulting nifti

"""
def main():
	nii_path = sys.argv[1] # path of image to normalize

	nii_folder = os.path.dirname(nii_path) # getting output folder
	nii_name = nii_path.split(os.path.sep)[-1] # getting nifti name
	result_name = rename_file(nii_name,'norm') # generating result name for normalized nifti
	final_nii = os.path.join(nii_folder,result_name) # generating result path for normalized nifti

	nii = nib.load(nii_path) # loading nii
	nii_matrix = nii.get_data() # loading nii matrix

	nii_copy = np.copy(nii_matrix) # making a copy of nii_matrix, to safely work in nii_copy matrix

	label_image = label(nii_copy == 0) 

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

	nii_matrix[:,:,:] = masked_nii

	nii.to_filename(final_nii) # saving resulting nifti


if __name__ == '__main__':
    main()
"""