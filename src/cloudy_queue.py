import numpy as np
import pathlib
import subprocess
import multiprocessing
from cloudy import CloudyInput

class QueueManager:
    def __init__(self, samples:np.array, N:int, target_dir:str,  ncpus:int=None, verbose:bool=True):
        # set number of cpus to use
        if not ncpus:
            self.ncpus = multiprocessing.cpu_count()
        else:
            self.ncpus = ncpus
        
        # set samples as attributes of the class
        self.samples = samples
        self.N = N

        # set the target directory
        self.target_dir = target_dir

        # verbosity level
        self.verbose = verbose
    
    def _create_in_files(self):

        if self.verbose: print("Creating the in files ...")
        self.in_files = []
        for idx, sample in enumerate(self.samples):
            in_file = CloudyInput(index=idx, N=self.N, target_dir=self.target_dir, LineList_path="../data/LineList_in.dat").create(*sample)
            self.in_files.append(in_file)
    
    def _run_in_file(self, in_file:str):

        try:
            """
            process = subprocess.Popen(['ping', '8.8.8.8'], 
                                    stderr=subprocess.PIPE, 
                                    stdout=subprocess.PIPE)
            """
            # /data/samples/../model.in
            # dir: data/samples/../
            # model.in
            dir_ = str(pathlib.Path(in_file).parent)
            #process = subprocess.Popen([f'cd {dir_} ; ~/c17.02/source/cloudy.exe model.in'])
            subprocess.call(f'cd {dir_} && ~/c17.02/source/cloudy.exe model.in', shell=True)
            

        except Exception as error:
            process.kill()
            message = "error: %s run(*%r, **%r)" % (e, args, kwargs)
            print(message)

    def _run(self):
        if self.verbose: print("Running the in files ...")
        pool = multiprocessing.Pool(processes=self.ncpus,
                               maxtasksperchild=1)
        if self.verbose: print('Initialized {} threads'.format(self.ncpus))
        pool.map(self._run_in_file, self.in_files)
        
        pool.close()
        pool.join()

    def run(self):
        self._create_in_files()
        self._run()


if __name__ == "__main__":

    from sampling import sampling_create_parameters

    target_directory = '../data/samples/'
    N = 10

    # Parameter names           Intervals                   Units
    # 1. Gas density            interval=[-3.0, 6.0]        log (cm^-3)
    # 2. Gas phase metallicity  interval=[-3.0, 0.30103]    Solar metallicity
    # 3. Redshift               interval=[3.0, 12.0]        Absolute value
    # 4. ionization parameter   interval=[-4.0, 0.0]        See Hazy 5.8
    # 5. Stellar metallicity    interval=[-5, -1.3979]      Absolute value
    # 6. Stellar age            interval=[1.0, 2000.0]      Myr

    samples = sampling_create_parameters(path=target_directory,
                               n_samples=N,
                               filter=True,
                               save_to_file=True,
                               plot=False
                               )
    
    queue = QueueManager(samples, N=N, target_dir=target_directory, verbose=True)
    queue.run()