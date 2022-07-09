import sys
import argparse
import pandas as pd
import seaborn as sns
import pathlib
import matplotlib
import matplotlib.pyplot as plt

sys.path.append('..')
sys.path.append('../src/')
from output_parser import OutputParser

# -----------------------------------------------------------------
#  Matplotlib settings
# -----------------------------------------------------------------
matplotlib.use('Agg')
usetex = matplotlib.checkdep_usetex(True)
matplotlib.rcParams['text.usetex'] = usetex


# -----------------------------------------------------------------
#  Parsing of a given run
# -----------------------------------------------------------------
def parse_run(N_sample, make_plots=False):

    # run directory for the sample
    run_dir_path = pathlib.Path(F'../data/samples/sample_N{N_sample}/')
    run_dir_path_abs = run_dir_path.resolve()

    if not run_dir_path_abs.is_dir():
        print(f"Directory {run_dir_path_abs} does not exist. Exiting", file=sys.stderr)
        exit(1)

    # create parser instance and run it
    output_parser = OutputParser()
    output_parser.parse(path=run_dir_path_abs)

    if make_plots:
        plot_run_times(path=run_dir_path_abs, N_sample=N_sample)


# -----------------------------------------------------------------
#  Optional: run time plot
# -----------------------------------------------------------------
def plot_run_times(path: pathlib.PosixPath, N_sample: int):

    status_file_path = path.joinpath("status.pkl")
    df = pd.read_pickle(status_file_path)

    # find run times for successful runs
    run_times_filtered = df['time'][df['status'] == 0]
    run_times_histogram = sns.histplot(data=run_times_filtered, binwidth=300, kde=True)
    run_times_histogram.set(xlabel="Run time [s]", ylabel="Model count")

    fig = run_times_histogram.get_figure()
    fig.set_size_inches(10, 7)
    figure_path = path.joinpath(F"run_times_filtered_{N_sample}.png")
    print(F"\nWriting plot of run times to file {figure_path}")
    fig.savefig(figure_path)
    fig.clear()


if __name__ == "__main__":

    # type in `python3 check_runs.py --N_sample 8000`
    parser = argparse.ArgumentParser()
    parser.add_argument("--N_sample", required=True, type=int,
                        help="Number of models in the sample. ")

    args = parser.parse_args()
    parse_run(args.N_sample, make_plots=True)
