"""
Example script to create a sample of Cloudy models and run them:

1. Generate a sample of input parameters
2. Create the respective model.in files for Cloudy to run
3. Run the model.in files with Cloudy using multiprocessing.
"""

import argparse
import sys
import os
from tqdm import tqdm

sys.path.append('..')
sys.path.append('../src/')
from src.cloudy_input import CloudyInput
from src.manager import QueueManager
from src.sampling import sampling_create_parameters
from common.utils import *


def main(args):

    # 1. set up directory sample / check if it exists
    sample_path, new_sample = utils_setup_sample_dir(parent_path=args.sample_parent_dir,
                                                     N_sample=args.N_sample)

    if not new_sample:

        print('Sample {} already exists, skipping sample generation'.format(sample_path))

    else:
        # 1a. generate parameter samples
        parameter_samples = sampling_create_parameters(path=sample_path,
                                                       N_sample=args.N_sample,
                                                       filter=True,
                                                       save_to_file=True,
                                                       plot=False)

        # 1b. create individual directories and generate input files for each model
        sample_todo_dir = os.path.join(sample_path, SAMPLE_SUBDIR_TODO)

        print('Creating model.in files in {}'.format(sample_todo_dir))
        for idx, sample in enumerate(tqdm(parameter_samples)):
            CloudyInput(index=idx,
                        N_sample=args.N_sample,
                        target_dir=sample_todo_dir,
                        LineList_path=args.line_list_path).create(*sample)

    # 2. create a queue of models and run them
    queue = QueueManager(sample_dir=sample_path,
                         N_CPUs=args.N_cpus,
                         N_batch=args.N_batch,
                         verbose=True)

    queue.manager_run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--N_sample", required=True, type=int,
                        help="Number of models in the sample. "
                             "Note: some parameter combinations will be filtered out due to not being physical)")

    parser.add_argument("--N_cpus", required=False, type=int,
                        help="Number of CPU cores to utilise")

    parser.add_argument("--N_batch", required=False, type=int,
                        help="Number of models to run (default: all)")

    my_args = parser.parse_args()

    my_args.sample_parent_dir = '../data/samples/'
    my_args.line_list_path = '../data/LineList_in.dat'

    main(my_args)





