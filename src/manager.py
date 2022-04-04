import pathlib
import subprocess
import multiprocessing
import numpy as np

from common.settings import CLOUDY_PATH
from common.utils import read_output
from cloudy import CloudyInput

class QueueManager:
    """ Class used to manage a queue of CLOUDY input models. It uses an array of samples to construct
    model.in files and runs them as subprocesses on multiple CPUs.

    :param numpy.array samples: numpy.array of dimension (m,n) where m is the number of samples and n is
    the dimension of the sample. A sample contains, in order: [Gas density, Gas phase metallicity,
    redshift, ionization parameter, stellar metallicity, stellar age]
    :param int N: int number of models to run (initially before the filter)
    :param str target_dir: string path to the folder where the samples are to be saved
    :param int npcus: int Maximum number of CPUS to use, if not defined it will use all available CPUS in the system.
    :param bool verbose: bool flag used to activate/deactivate the verbosity. Defaults to True (verbose)
    """
    def __init__(self, target_dir:str="data/sampes/sample_N4000",  ncpus:int=None, verbose:bool=True):

        # set number of cpus to use, if not defined use all avalable
        if not ncpus:
            self.ncpus = multiprocessing.cpu_count()
        else:
            self.ncpus = ncpus

        self.target_dir = target_dir    # set the target directory
        self.verbose = verbose          # verbosity level

    def _get_infiles(self):
        """ Looks inside the todo/ directory, iterates over all item in directory
        and appends them into a buffer if they are a subdirectory and not a file.
        e.g if target directory is ".../data/samples/sample_Nxxx"
        then will iterate over all directories ".../data/samples/sample_Nxxx/todo/x"
        and append them to a list of model.in paths e.g ".../data/samples/sample_Nxxx/todo/x/model.in"
        """
        directory = pathlib.Path(self.target_dir, "todo")
        assert directory.exists(), f'Couldnt find todo/ directory in {self.target_dir}.'
        self.in_files = []
        for item in directory.iterdir():
            if item.is_dir():
                self.in_files.append(str(pathlib.Path(item, 'model.in')))

    def _run_in_file(self, in_file:str) -> None:
        """ Private method. Given the model.in path open a subprocess
        and run it there with CLOUDY.
        :param in_file: string path to the model.in file to be run by CLOUDY
        """
        try:
            # CLOUDY doesn't accept paths to the model.in files, so here we cd to the
            # directory where the model.in file is (dir_) and run cloudy from there.
            dir_ = str(pathlib.Path(in_file).parent)
            subprocess.call(f'cd {dir_} && {CLOUDY_PATH} model.in', shell=True)

        # manage exception
        except Exception as error:
            process.kill()
            message = "error: %s run(*%r, **%r)" % (e, args, kwargs)
            print(message)

    def _run(self) -> None:
        """ Private method called by the public method self.run(). When called it runs all created
        model.in files using CLOUDY on as may CPUs as defined (user-defined maximum or systen maximum)
        """
        pool = multiprocessing.Pool(processes=self.ncpus,
                               maxtasksperchild=1)
        if self.verbose: print('Initialized {} threads'.format(self.ncpus))
        pool.map(self._run_in_file, self.in_files)

        pool.close()
        pool.join()

    def run(self) -> None:
        """ Main method of the class, it wraps the private methods to read the files and run the files."""
        if self.verbose: print("Reading the input files ...")
        self._get_infiles()
        if self.verbose: print(f"---- {len(self.in_files)} model.in files found ----")
        if self.verbose: print("Running the model.in files ...")
        self._run()             # runs all created model.in files in multiple CPUs

    def _check_run(self):
        """Checks the target_dir for cloudy runs; writes out successful and failed run folders to dictionary file with summary message.
        """

        try:
            pathlib.Path(f'{self.target_dir}/todo').mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            if self.verbose: print("Folder exists")
            req_dir=f'{self.target_dir}/todo'
            exists=True
        else:
            if self.verbose: print("Folder created")
            req_dir=self.target_dir
            exists=False

        sample_files=get_files(req_dir)
        to_do={}
        run_ok={}
        ii=0
        for sample_file in sample_files:
            last_line=read_output(sample_file)
            if last_line=='':
                to_do[sample_file]='Empty'
            elif 'ABORT' in last_line:
                to_do[sample_file]='Cloudy Error'
            elif "Cloudy exited OK" not in last_line:
                to_do[sample_file]='Time up'

            if "Cloudy exited OK" in last_line:
                run_ok[sample_file]='OK'
                ii+=1

        if self.verbose: print(f'{len(sample_files-ii)} models failed to run')
        np.save(f'{self.target_dir}/ok.npy', run_ok)
        np.save(f'{self.target_dir}/todo.npy', to_do)

        if exists:
            for key in run_ok:
                subprocess.call(f'mv {key} {self.target_dir}/', shell=True)
        else:
            for key in to_do:
                subprocess.call(f'mv {key} {self.target_dir}/todo', shell=True)
