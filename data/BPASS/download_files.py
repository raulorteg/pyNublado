import gdown


def download_bpass():
    """
    Attemps to download the BPASS files
    Returns: None
    """
    url = "https://drive.google.com/uc?id=1wGpW9j4Ts4AL947s1rUQCfKc76V4LqV4"

    output = "bpass_v2.2.1_imf135_100.tar.gz"

    gdown.download(url, output, quiet=False)


if __name__ == "__main__":

    download_bpass()