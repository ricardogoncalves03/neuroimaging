Module preprocessing.skull_stripping
====================================

Classes
-------

`SkullStripping(img: str, robex_path: str)`
:   Skull stripping using ROBEX tool - https://www.nitrc.org/projects/robex
    
    Initializes a skull stripping object, where `img_path` is the path to the NIfTI image,
    and `robex_path` is the path to the file runROBEX.sh

    ### Ancestors (in MRO)

    * preprocessing.path.Path

    ### Methods

    `output(self) ‑> Tuple[str, str]`
    :   Start skull stripping process