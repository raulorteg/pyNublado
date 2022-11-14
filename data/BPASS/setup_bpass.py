import os
import gdown
import sys
import hashlib
import shutil
from pathlib import Path

sys.path.append("../../src/")
from user_settings import STELLAR_MODEL_DIR, STELLAR_MODEL_MOD_FILE, CLOUDY_PATH

BPASS_ARCHIVE_FILE = "bpass_v2.2.1_imf_chab300.tar.gz"
BPASS_ARCHIVE_MD5 = "2c10b1afa915b23e88fc9675916159d7"
BPASS_ASCII_FILE_TMP = "BPASS_burst_binary.ascii"

COMPILE_IN_FILE = "compile_BPASS.in"


def _download_bpass():
    """
    Attempts to download the BPASS files
    Returns: None
    """

    p = Path(BPASS_ARCHIVE_FILE)

    if p.exists() and _get_file_md5_hash(p) == BPASS_ARCHIVE_MD5:
        pass
        print(F"No need to download, {BPASS_ARCHIVE_FILE} already exists")
    else:
        url = "https://drive.google.com/uc?id=1JcUM-qyOQD16RdfWjhGKSTwdNfRUW4Xu"


        gdown.download(url, output=BPASS_ARCHIVE_FILE, quiet=False, fuzzy=True)

    os.system(F"tar -xvf {BPASS_ARCHIVE_FILE}")


def _convert_bpass():
    """
    Attempts to run the Perl ascii conversion script on the downloaded files
    Returns: None
    """
    os.system("chmod +x convert_bpassv2.x.pl")

    # create ascii files
    os.system("./convert_bpassv2.x.pl")

    # delete unnecessary files
    os.system("rm *.dat.gz")
    os.system("rm input_bpass_z*_bin_imf_chab300")
    os.system("rm input_bpass_z*_sin_imf_chab300")


def _compile_bpass():
    """
    Checks if the target directories for teh stellar atmospheres model exist,
    moves the previously generated ascii file from the BPASS directory to the
    Cloudy data directory and compiles it there into a binary model that
    Cloudy can use.
    Returns: None
    """

    # check if ascii file exists
    ascii_path = Path(BPASS_ASCII_FILE_TMP)
    if not ascii_path.exists() or ascii_path.is_dir():
        raise FileNotFoundError

    # find path to the Cloudy data dir
    cloudy_exe_path = Path(CLOUDY_PATH).expanduser()

    cloudy_install_path = cloudy_exe_path.parent.parent
    cloudy_data_path = cloudy_install_path.joinpath('data')

    if not cloudy_data_path.exists():
        raise Exception(F"Can't find Cloudy data directory. Exiting")

    # check if STELLAR_MODEL_DIR exists
    cloudy_stellar_model_path = cloudy_data_path.joinpath(STELLAR_MODEL_DIR)
    if not cloudy_stellar_model_path.exists():
        print(F"{STELLAR_MODEL_DIR} directory does not exist. Trying to create it ...")
        try:
            cloudy_stellar_model_path.mkdir(mode=0o777, parents=True)
        except PermissionError:
            print(F"Error: Could not create directory {STELLAR_MODEL_DIR}. Permission denied.")
            exit(1)

    # rename and copy the ascii file to the Cloudy data dir
    target_ascii_path = Path.joinpath(cloudy_stellar_model_path, F"{Path(STELLAR_MODEL_MOD_FILE).stem}.ascii")
    shutil.copy(str(ascii_path), str(target_ascii_path))

    # cd to the data directory & create the .in file for cloudy to compile
    os.chdir(cloudy_data_path)

    cloudy_compile_cmd = F"compile star \"{STELLAR_MODEL_DIR}/{target_ascii_path.name}\"\n"

    with open(F"{COMPILE_IN_FILE}", "w") as f:
        f.write(cloudy_compile_cmd)

    # run cloudy on the .in file
    print(F"Compiling binary stellar atmosphere module with Cloudy")
    os.system(F"{cloudy_exe_path} {COMPILE_IN_FILE}")

    print(F"Done")
    # TODO: check if outfile exists and cloudy exited okay.


def _get_file_md5_hash(file_path):
    """
    Calculates the md5 hash for a given file, assuming it exists.
    Args: pathlib Path object to be checked
    Returns: Hex string representation of the MD5 hash
    """
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)

    return str(file_hash.hexdigest())


if __name__ == "__main__":

    _download_bpass()
    _convert_bpass()
    _compile_bpass()
