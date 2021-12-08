Module preprocessing.registration
=================================

Classes
-------

`Registration(fixed_img: str, moving_img: str)`
:   Class to register two NIfTI images, producing a rigid registration which is going to be improved by an
    affine registration order 0. Tool used is SimpleElastix (https://simpleelastix.github.io/)
    
    Initializes a registration object, where `fixed_img` is the image used as baseline
    and `moving_img` is the image we want to register

    ### Ancestors (in MRO)

    * preprocessing.path.Path

    ### Methods

    `output(self) ‑> str`
    :

    `start(self) ‑> None`
    :   Start registration process with both rigid and affine