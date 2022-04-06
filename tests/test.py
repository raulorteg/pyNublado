import sys
sys.path.append("..")
sys.path.append("../src")

import os, pathlib, shutil
import time
import pytest
from src.common.settings import CLOUDY_PATH, SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE
from src.manager import QueueManager


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
    time.sleep(30)

    # assert number of models run is ok
    assert queue.N_models_to_run == 4, "Some models did not get identified by the _get_models() method."

    # check all directories that need to be created exist
    for dir_ in [ SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE ]:
        assert os.path.exists(f"tmp_data/sample_N100/{dir_}"), f"{dir_} directory could not be found"

    # check all directories that need to be empty are so
    for dir_ in [SAMPLE_SUBDIR_TODO]:
        assert len(os.listdir(f'tmp_data/sample_N100/{dir_}/')) == 0, f"Some models remain in {dir_} folder"

# TODO: more tests here ...


if __name__ == "__main__":
    test_queue_manager()
