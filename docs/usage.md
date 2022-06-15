### Usage

```
import sys, os

sys.path.append('..')
sys.path.append('../src/')
from src.cloudy_input import CloudyInput
from src.manager import QueueManager
from src.sampling import sampling_create_parameters
from common.utils import *

if __name__ == "__main__"

    # 1. Sampling the CLOUDY input parameter space
    # set up directory sample
    sample_path, new_sample = utils_setup_sample_dir(parent_path=args.sample_parent_dir,        N_sample=args.N_sample)

    # 1a. generate parameter samples
    parameter_samples = sampling_create_parameters(path=sample_path,
                                                    N_sample=args.N_sample,
                                                    filter=True,
                                                    save_to_file=True,
                                                    plot=False)

    # 1b. create individual directories and generate input files for each model
    sample_todo_dir = os.path.join(sample_path, SAMPLE_SUBDIR_TODO)

    print('Creating *.in files in {}'.format(sample_todo_dir))
    for idx, sample in enumerate(parameter_samples):
        CloudyInput(index=idx,
                    N_sample=args.N_sample,
                    target_dir=sample_todo_dir,
                    LineList_path=args.line_list_path).create(*sample)

    # 2. Running the CLOUDY models
    # create a queue of models and run them
    queue = QueueManager(sample_dir=sample_path,
                         N_CPUs=args.N_cpus,
                         N_batch=args.N_batch,
                         verbose=True)

    queue.manager_run()
```
