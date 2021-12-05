from preprocessing.registration import Registration
from preprocessing.skull_stripping import SkullStripping


def main():
    ### TEST registration module - needs to be tested on server
    fixed_img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_registration/a012/t1.nii.gz"
    moving_img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_registration/a012/flair.nii.gz"

    registration = Registration(fixed_img, moving_img)
    registration.rigid_registration()
    registration.affine_registration()
    registered_img = registration.output()
    registration.remove_files()

    """
    ### Skull stripping module working
    img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/a012/flair.nii.gz"
    robex = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/ROBEXv12.linux64/ROBEX/runROBEX.sh"
    ss = SkullStripping(img, robex)
    ss.start()
    """


if __name__ == '__main__':
    main()
