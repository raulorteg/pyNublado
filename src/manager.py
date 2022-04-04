import pathlib
import subprocess
import multiprocessing
import numpy as np
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
    def __init__(self, samples:np.array, N:int, target_dir:str,  ncpus:int=None, verbose:bool=True):
        
        # set number of cpus to use, if not defined use all avalable
        if not ncpus:
            self.ncpus = multiprocessing.cpu_count()
        else:
            self.ncpus = ncpus
        
        self.samples = samples          # set samples as attributes of the class
        self.N = N                      # number of samples
        self.target_dir = target_dir    # set the target directory
        self.verbose = verbose          # verbosity level
    
    def _create_in_files(self) -> None:
        """ Private method called by self._run(). When called create all the model.in files from the list of samples
        and save the path to each model.in file in a buffer attribute of the class
        so they can be run later.
        """
        if self.verbose: print("Creating the in files ...")
        self.in_files = [] # buffer where the paths to model.in files are stored

        # for all samples create the model.in file to be run by cloudy
        # and append the path where the model.in file is to the buffer so we know its location
        for idx, sample in enumerate(self.samples):
            in_file = CloudyInput(index=idx, N=self.N, target_dir=self.target_dir, LineList_path="../data/LineList_in.dat").create(*sample)
            self.in_files.append(in_file)
    
    def _run_in_file(self, in_file:str) -> None:
        """ Private method. Given the model.in path open a subprocess
        and run it there with CLOUDY.
        :param in_file: string path to the model.in file to be run by CLOUDY
        """
        try:
            # CLOUDY doesn't accept paths to the model.in files, so here we cd to the
            # directory where the model.in file is (dir_) and run cloudy from there.
            dir_ = str(pathlib.Path(in_file).parent)
            subprocess.call(f'cd {dir_} && ~/c17.02/source/cloudy.exe model.in', shell=True)

        # manage exception
        except Exception as error:
            process.kill()
            message = "error: %s run(*%r, **%r)" % (e, args, kwargs)
            print(message)

    def _run(self) -> None:
        """ Private method called by the public method self.run(). When called it runs all created
        model.in files using CLOUDY on as may CPUs as defined (user-defined maximum or systen maximum)
        """
        if self.verbose: print("Running the in files ...")
        pool = multiprocessing.Pool(processes=self.ncpus,
                               maxtasksperchild=1)
        if self.verbose: print('Initialized {} threads'.format(self.ncpus))
        pool.map(self._run_in_file, self.in_files)
        
        pool.close()
        pool.join()

    def run(self) -> None:
        """ Main method of the class, it wraps the private methods to create the files and run the files."""
        self._create_in_files() # creates all model.in files and recors their paths
        self._run()             # runs all created model.in files in multiple CPUs