from preprocessing.n4_correction import N4Correction
# from preprocessing.registration import Registration
# from preprocessing.skull_stripping import SkullStripping


def main():
    """
    ### ************Made some changes to registration module - needs to be tested again on server
    fixed_img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_registration/a012/t1.nii.gz"
    moving_img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_registration/a012/flair.nii.gz"
    registration = Registration(fixed_img, moving_img)
    registration.start()
    registered_img = registration.output()
    ###

    ### Skull stripping module working
    img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/a012/flair.nii.gz"
    robex = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/ROBEXv12.linux64/ROBEX/runROBEX.sh"
    ss = SkullStripping(img, robex)
    ss.start()
    ###
    """

    ### N4 filter
    img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_n4/ss_flair.nii.gz"
    mask = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_n4/mask_flair.nii.gz"
    n4 = N4Correction(img, mask)
    # n4.cast()
    n4.output()


if __name__ == '__main__':
    main()
