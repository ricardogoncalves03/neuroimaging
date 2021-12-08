from preprocessing.n4_correction import N4Correction
# from preprocessing.registration import Registration
from preprocessing.skull_stripping import SkullStripping
from preprocessing.normalization import Normalization


def main():
    # -----------------PREPROCESSING EXAMPLE FOR flair.nii.gz----------------- #

    ### Skull stripping
    img_flair = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_ss/a012/flair.nii.gz"
    robex = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_ss/ROBEXv12.linux64/ROBEX/runROBEX.sh"
    ss = SkullStripping(img_flair, robex)
    img_tup = ss.output()
    ss_flair = img_tup[0]
    ss_flair_mask = img_tup[1]
    print(ss_flair, ss_flair_mask)


    """
    ### ************Made some changes to registration module - needs to be tested again on server
    fixed_img = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_registration/a012/t1.nii.gz"
    moving_img = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_registration/a012/flair.nii.gz"
    registration = Registration(fixed_img, moving_img)
    registration.start()
    registered_img_flair = registration.output()
    ###
    ### Skull stripping
    img_flair = registered_img_flair
    robex = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_ss/ROBEXv12.linux64/ROBEX/runROBEX.sh"
    ss = SkullStripping(img, robex)
    ss.start()
    ss_flair = ss.start[0]
    ss_flair_mask = ss.start[1]
    ###
    ### N4 filter
    n4 = N4Correction(ss_flair, ss_flair_mask)
    n4.cast()
    n4_flair = n4.output()
    ###
    """

    ### Normalization not working
    #img = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_normalization/a012/flair.nii.gz"
    #img_ss = "/home/ricardo/Documents/neuroimaging-tests/preprocessing/test_ss/a012/ss_flair.nii.gz"
    #norm = Normalization(img_ss)
    #norm.start()


if __name__ == '__main__':
    main()
