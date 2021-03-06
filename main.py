from preprocessing import (
    Registration, SkullStripping, N4Correction, Normalization
    )


def main():
    # -----------------PREPROCESSING EXAMPLE FOR a single flair.nii.gz----------------- #

    # Registration
    fixed_img = "/PATH/t1.nii.gz"
    moving_img = "/PATH/flair.nii.gz"
    registration = Registration(fixed_img, moving_img)
    registration.start()
    registered_img_flair = registration.output()

    # Skull stripping
    robex = "/PATH/ROBEX/runROBEX.sh"
    ss = SkullStripping(registered_img_flair, robex)
    flair_tup = ss.output()
    ss_flair = flair_tup[0]
    ss_flair_mask = flair_tup[1]

    # N4 filter
    n4 = N4Correction(ss_flair, ss_flair_mask)
    n4_flair = n4.output()

    # Normalization
    norm = Normalization(n4_flair)
    norm.start()
    norm.output()


if __name__ == '__main__':
    main()
