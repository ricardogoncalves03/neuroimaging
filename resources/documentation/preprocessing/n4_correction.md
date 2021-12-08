Module preprocessing.n4_correction
==================================

Classes
-------

`N4Correction(img: str, mask: str)`
:   Class that implements N4 bias field correction algorithm.
    More info here: https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html
    
    Initializes a n4 bias field correction object, where `img` is the image to be corrected
    and `mask` is the image mask to help with the correction.

    ### Ancestors (in MRO)

    * preprocessing.path.Path

    ### Methods

    `output(self) ‑> str`
    :   Image output