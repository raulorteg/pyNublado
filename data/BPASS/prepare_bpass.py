import os
import gdown

BPASS_FILE = "bpass_v2.2.1_imf_chab300.tar.gz"


def download_bpass():
    """
    Attempts to download the BPASS files
    Returns: None
    """
    url = "https://drive.google.com/uc?id=1JcUM-qyOQD16RdfWjhGKSTwdNfRUW4Xu"

    gdown.download(url, output=BPASS_FILE, quiet=False, fuzzy=True )


def unpack_bpass():

    os.system(F"tar -xvf {BPASS_FILE}")


def convert_bpass():

    os.system("chmod +x convert_bpassv2.x.pl")

    # create ascii files
    os.system("./convert_bpassv2.x.pl")

    # clean up
    os.system("rm *.dat.gz")


if __name__ == "__main__":

    #TODO: add error handling

    download_bpass()
    unpack_bpass()
    convert_bpass()
