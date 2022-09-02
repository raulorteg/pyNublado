import os
import gdown

BPASS_FILE = "bpass_v2.2.1_imf135_100.tar.gz"


def download_bpass():
    """
    Attempts to download the BPASS files
    Returns: None
    """
    url = "https://drive.google.com/uc?id=1wGpW9j4Ts4AL947s1rUQCfKc76V4LqV4"

    gdown.download(url, output=BPASS_FILE, quiet=False)


def unpack_bpass():

    os.system(F"tar -xvf {BPASS_FILE}")


def convert_bpass():

    os.system("chmod +x convert_bpassv2.x.pl")
    os.system("./convert_bpassv2.x.pl")


if __name__ == "__main__":

    #TODO: add error handling

    download_bpass()
    unpack_bpass()
    convert_bpass()
