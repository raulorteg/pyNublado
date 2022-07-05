import os
import pathlib
import subprocess
import multiprocessing
import numpy as np
import traceback

from common.settings import SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE
from common.utils import *
from cloudy_input import CloudyInput
from user_settings import CLOUDY_PATH, CLOUDY_RUN_TIMEOUT


class QueueManager:
    """ Class used to manage a queue of Cloudy input models.

    It uses the directory containing a sample of models, creates a queue of runs to be performed,
    and runs subprocesses on multiple CPU cores.

    :param str sample_dir: string path to the folder where the samples are to be saved
    :param int N_CPUs: int Maximum number of CPUS to use, if not defined it will use all available CPUS in the system.
    :param int N_batch: int Number of models to run. If not specified or larger than the total number of models, all
                        models will be run.
    :param bool verbose: bool flag used to activate/deactivate the verbosity. Defaults to True (verbose)
    """
    def __init__(self, sample_dir: str,  N_CPUs: int = None, N_batch: int = None, verbose: bool = True):

        if not N_CPUs:
            # if not specified, use all available CPU cores
            self.N_CPUs = multiprocessing.cpu_count()
        else:
            self.N_CPUs = N_CPUs

        self.sample_dir = sample_dir    # set the target directory
        self.verbose = verbose          # verbosity level

        if N_batch:
            self.N_batch = N_batch
        else:
            self.N_batch = None

    def _get_models(self):
        """
        Looks inside the SAMPLE_SUBDIR_TODO/ directory, iterates over all items in the directory
        and appends the model directory to a list of models to run if
            1. they are a subdirectory and not a file and
            2. they contain a model.in file
        """
        directory = pathlib.Path(self.sample_dir, SAMPLE_SUBDIR_TODO)
        assert directory.exists(), f'Could not find {SAMPLE_SUBDIR_TODO}/ directory in {self.sample_dir}.'
        self.models_to_run = []

        for item in directory.iterdir():
            if item.is_dir():
                if CLOUDY_IN_FILE in os.listdir(item):
                    # save only the model folder name, not the path
                    p = pathlib.PurePath(item).name
                    self.models_to_run.append(p)

        self.N_models_to_run = len(self.models_to_run)

        # if maximum number of models to run specified, then run a subset of all models
        # check also this max is not greater than all models that are to be run
        if (self.N_batch) and (self.N_batch < self.N_models_to_run):
            self.models_to_run = self.models_to_run[:self.N_batch]
        
        self.N_models_to_run = len(self.models_to_run)

    def _run_model(self, model_dir: str) -> None:
        """ Private method that will launch a subprocess to run the Cloudy model.

        Since Cloudy doesn't seem to accept paths to the model.in files as an input, we cd to the
        directory that contains the model.in file is located, i.e. sample_N123/todo/42/ and run
        Cloudy from there.

        :param model_dir: string name of the model directory containing the model.in file
        """

        try:
            original_dir = os.getcwd()
            sample_dir = os.path.abspath(self.sample_dir)

            if self.verbose: print(f' Running model {model_dir} ...')

            current_run_dir = os.path.join(sample_dir, SAMPLE_SUBDIR_TODO, model_dir)

            os.chdir(current_run_dir)
            cmd_string = f'{CLOUDY_PATH} model.in'

            try:
                subprocess.call(cmd_string, shell=True, timeout=CLOUDY_RUN_TIMEOUT)
            except subprocess.TimeoutExpired:
                # catch time out, then continue and move the model directory
                if self.verbose: print(f' Time out reached while processing model {model_dir}')
                pass

            # Assuming the process terminated successfully, we are moving the model
            if self.verbose: print(f' Moving model {model_dir} to {SAMPLE_SUBDIR_DONE} directory')

            os.chdir(sample_dir)
            cmd_string = f' mv {SAMPLE_SUBDIR_TODO}/{model_dir} {SAMPLE_SUBDIR_DONE}/'
            subprocess.call(cmd_string, shell=True)

            # go back to original dir
            os.chdir(original_dir)

        # catch all other exceptions
        # TODO: specify more / different cases here once they arise (see traceback output)
        except Exception:
            if self.verbose:
                print(f' Error: while processing model {model_dir}')
                traceback.print_exc()

    def _run(self) -> None:
        """ Private method called by the public method self.manager_run().
        When called it runs all created models using Cloudy on as may CPUs as defined,
        user-defined maximum or system maximum.
        """

        if self.N_models_to_run:
            if self.verbose: print('Initialising {} threads'.format(self.N_CPUs))
            pool = multiprocessing.Pool(processes=self.N_CPUs, maxtasksperchild=1)

            pool.map(func=self._run_model, iterable=self.models_to_run, chunksize=1)

            pool.close()
            pool.join()

    def _check_run(self):
        """Checks the sample_dir for cloudy runs.
        Writes out successful and failed run folders to dictionary file with summary message.
        """
        # TODO: use SAMPLE_SUBDIR_* variables, modify to check runs in sample_N123/running

        try:
            pathlib.Path(f'{self.sample_dir}/{SAMPLE_SUBDIR_TODO}').mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            if self.verbose: print("Folder exists")
            req_dir = f'{self.sample_dir}/{SAMPLE_SUBDIR_TODO}'
            exists = True
        else:
            if self.verbose: print("Folder created")
            req_dir = self.sample_dir
            exists = False

        sample_files = utils_get_folders(req_dir)
        to_do = {}
        run_ok = {}
        ii = 0
        for sample_file in sample_files:
            last_line = utils_read_output(sample_file)
            if last_line == '':
                to_do[sample_file] = 'Empty'
            elif 'ABORT' in last_line:
                to_do[sample_file] = 'Cloudy Error'
            elif "Cloudy exited OK" not in last_line:
                to_do[sample_file] = 'Time up'

            if "Cloudy exited OK" in last_line:
                run_ok[sample_file] = 'OK'
                ii += 1

        if self.verbose: print(f'{len(sample_files-ii)} models failed to run')
        np.save(f'{self.sample_dir}/ok.npy', run_ok)
        np.save(f'{self.sample_dir}/todo.npy', to_do)

        if exists:
            for key in run_ok:
                subprocess.call(f'mv {key} {self.sample_dir}/', shell=True)
        else:
            for key in to_do:
                subprocess.call(f'mv {key} {self.sample_dir}/{SAMPLE_SUBDIR_TODO}', shell=True)

    def manager_run(self) -> None:
        """ Main method of the class, it wraps the private methods to read the files and run the files."""
        if self.verbose: print("Reading the input files ...")

        self._get_models()

        if self.verbose:
            print(f"Found {self.N_models_to_run} models to run ")

        self._run()  # runs all created model.in files in multiple CPUs
