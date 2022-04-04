### Usage

Example script
```
from pynublado.manager import QueueManager
from pynublado.sampling import sampling_create_parameters

target_directory = '../data/samples/'
N = 100

# create the samples (combination of input parmeters to run)
samples = sampling_create_parameters(path=target_directory,
                               n_samples=N,
                               filter=True,
                               save_to_file=True,
                               plot=False
                               )
    
# create and run the models for this combinations
queue = QueueManager(samples, N=N, target_dir=target_directory, verbose=True)
queue.run()
```
