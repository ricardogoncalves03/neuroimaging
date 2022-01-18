# Neuroimaging

Preprocessing pipeline for medical imaging.

----
# Table of Contents

1. [Registration](#registration)

2. [Skull Stripping](#skull-stripping)

3. [N4 Filter](#n4-filter)

4. [Normalization](#normalization)

5. [Usage](#usage)

6. [Dependencies](#dependencies)

<br><br>

# Registration

Image registration of NIfTI images, producing a rigid registration which is going to be improved by an affine registration order 0.
The tool used to produce the registration is [SimpleElastix](https://simpleelastix.github.io/).

<br><br>

# Skull Stripping

Skull stripping using [ROBEX](https://www.nitrc.org/projects/robex).

<br><br>

# N4 Filter

[N4 bias field correction algorithm](https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html) 
for correcting low frequency intensity non-uniformity present in MRI image.

<br><br>

# Normalization

Image normalization according to [Qtim deep learning tutorial](https://github.com/QTIM-Lab/qtim_Tutorials). 
Results will have 0 mean, min intensity of around -2 and max intensity of around 2.

<br><br>

# Usage

Refer to the _main.py_ for an example of a single image preprocessing using all the steps listed above. 
There is also a structured documentation inside the resources/documentation directory. 

<br><br>

# Dependencies

* scikit-image - ```pip install scikit-image```
* scikit-learn - ```pip install scikit-learn```
* nibabel - ```pip install nibabel```
* numpy - ```pip install numpy```
* SimpleITK - ```pip install SimpleITK```
