if __name__ == "__main__":

    from cloudy_queue import QueueManager
    from sampling import sampling_create_parameters
    import argparse

    import argparse
    # parsing user input
    # example: python script_hpc.py --N=100
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", required=True, type=int)
    args = parser.parse_args()

    target_directory = '../data/samples/'
    N = args.N

    samples = sampling_create_parameters(path=target_directory,
                               n_samples=N,
                               filter=True,
                               save_to_file=True,
                               plot=False
                               )
    queue = QueueManager(samples, N=N, target_dir=target_directory, verbose=True)
    queue.run()