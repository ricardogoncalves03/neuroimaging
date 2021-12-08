from preprocessing.n4_correction import N4Correction
from preprocessing.registration import Registration
from preprocessing.skull_stripping import SkullStripping
from preprocessing.normalization import Normalization
from preprocessing.normalize import Normalize


def main():
    # -----------------PREPROCESSING EXAMPLE FOR flair.nii.gz----------------- #

    """
    ### ************Made some changes to registration module - needs to be tested again on server
    fixed_img = "/PATH/t1.nii.gz"
    moving_img = "/PATH/flair.nii.gz"
    registration = Registration(fixed_img, moving_img)
    registration.start()
    registered_img_flair = registration.output()
    ###
    ### Skull stripping
    img_flair = registered_img_flair
    robex = "/PATH/ROBEX/runROBEX.sh"
    ss = SkullStripping(img_flair, robex)
    flair_tup = ss.output()
    ss_flair = flair_tup[0]
    ss_flair_mask = flair_tup[1]
    ###
    ### N4 filter
    n4 = N4Correction(ss_flair, ss_flair_mask)
    n4.cast()
    n4_flair = n4.output()
    ###
    ### Normalization not working
    norm = Normalization(n4_flair)
    norm.start()
    norm_flair = norm.output()
    """


if __name__ == '__main__':
    main()
