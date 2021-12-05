from pathname import path
from preprocessing.skull_stripping import SkullStripping
from pathname.path import Directory

def main():
    img = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/a012/flair.nii.gz"
    robex = "/home/ricardo/Documents/neuroImaging-tests/preprocessing/test_ss/ROBEXv12.linux64/ROBEX/runROBEX.sh"


    a = Directory.get_path()
    b = Directory.get_name()

    # ss = SkullStripping(img, robex)
    # ss.start()


if __name__ == '__main__':
    main()
