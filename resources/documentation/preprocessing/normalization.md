Module preprocessing.normalization
==================================

Classes
-------

`Normalization(img: str)`
:   Class to normalize NIfTI images according to Qtim deep learning tutorial.
    Results will have 0 mean, min intensity of around -2 and max intensity of around 2
    
    Initializes a normalization object, where `img` is the img to be normalized,
    `nii` is the image loaded using nibabel, so it can be manipulated and `nii_matrix`
    is the image matrix info

    ### Ancestors (in MRO)

    * preprocessing.path.Path

    ### Methods

    `output(self) ‑> str`
    :   Normalized img output

    `start(self) ‑> None`
    :   Start loading nii and masking it