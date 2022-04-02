"""
Example script to run the sampling of CLOUDY space.
1. Get the combinations of input parameters to be run
2. Create the model.in files for CLOUDY to run
3. Run the model.in files with CLOUDY using multiprocessing.
"""

if __name__ == "__main__":

    from cloudy_queue import QueueManager
    from sampling import sampling_create_parameters

    import argparse
    # example: python script_hpc.py --N=100
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", required=True, type=int, help="Number of samples to run (Note: some combinations will be filtered out due to not being Physical.)")
    args = parser.parse_args()

    # other inputs
    target_directory = '../data/samples/'
    N = args.N

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