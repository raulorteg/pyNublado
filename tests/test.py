import os, pathlib, shutil
import time
import pytest

import sys
sys.path.append("..")
sys.path.append("../src")

from src.common.settings import SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE
from user_settings import CLOUDY_PATH, STELLAR_MODEL_DIR, STELLAR_MODEL_MOD_FILE
from src.manager import QueueManager

Q_MANAGER_TEST_TIME_SECONDS = 60


def test_cloudy_runs():
    # check no model.out file exists
    if os.path.exists("model.out"):
        os.remove("model.out")
    
    # create the model.in test
    with open("model.in", "w") as f:
        print("test", file=f)
    
    # run it on cloudy
    command = CLOUDY_PATH + " model.in"
    os.popen(command).read()
    
    # check there was an model.out generated
    assert os.path.exists("model.out"), "No model.out was generated, Cloudy did not run."


def test_cloudy_exits_ok():
    # check no model.out file exists
    if os.path.exists("model.out"):
        os.remove("model.out")
    
    # create the model.in test
    with open("model.in", "w") as f:
        print("test", file=f)
    
    # run it on cloudy
    command = CLOUDY_PATH + " model.in"
    os.popen(command).read()

    # check the model.out exited OK
    with open("model.out", "r") as f:
        line = f.readlines()[-1]
    assert ("Cloudy exited OK" in line), "Cloudy run but failed."

    # clean up everything
    for file_ in ["model.in", "model.out"]:
        if os.path.exists(file_):
            os.remove(file_)


def test_queue_manager():

    # rm file structure if present
    if os.path.exists('tmp_data/'):
        shutil.rmtree('tmp_data/')

    # create the file structure
    dir_todo = ["0", "1", "2", "3"]
    for dir_ in dir_todo:
        dir_ = "tmp_data/sample_N100/todo/"+dir_
        pathlib.Path(dir_).mkdir(parents=True, exist_ok=True)

        with open(dir_+"/model.in", "w") as f:
            print("test", file=f)
    
    # run test models
    queue = QueueManager(sample_dir="tmp_data/sample_N100", N_CPUs=4, verbose=False)
    queue.manager_run()

    # wait for the models to finish
    time.sleep(Q_MANAGER_TEST_TIME_SECONDS)

    # assert number of models run is ok
    assert queue.N_models_to_run == 4, "Some models did not get identified by the _get_models() method."

    # check all directories that need to be created exist
    for dir_ in [SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE]:
        assert os.path.exists(f"tmp_data/sample_N100/{dir_}"), f"{dir_} directory could not be found"

    # check all directories that need to be empty are so
    for dir_ in [SAMPLE_SUBDIR_TODO]:
        assert len(os.listdir(f'tmp_data/sample_N100/{dir_}/')) == 0, f"Some models remain in {dir_} folder"

    # clean up everything
    if os.path.exists('tmp_data/'):
        shutil.rmtree('tmp_data/')


def test_bpass_exists():

    cloudy_exe_path = pathlib.Path(CLOUDY_PATH).expanduser()
    cloudy_install_path = cloudy_exe_path.parent.parent
    cloudy_data_path = cloudy_install_path.joinpath('data')

    assert cloudy_data_path.exists(), F"Unable to find Cloudy data directory {cloudy_data_path}"

    # check if STELLAR_MODEL_DIR exists
    cloudy_stellar_model_dir_path = cloudy_data_path.joinpath(STELLAR_MODEL_DIR)
    assert cloudy_stellar_model_dir_path.exists(), \
        F"Unable to find Stellar model directory {cloudy_stellar_model_dir_path}"

    # check if STELLAR_MODEL_MOD_FILE exists
    cloudy_stellar_model_file_path = cloudy_stellar_model_dir_path.joinpath(STELLAR_MODEL_MOD_FILE)
    assert cloudy_stellar_model_file_path.exists(), \
        F"Unable to find Stellar model file {cloudy_stellar_model_file_path}"

# TODO: more tests here ...
