import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
from tqdm import tqdm

sys.path.append('..')
sys.path.append('../src/')
from common.settings_parameters import *
from common.settings import SAMPLE_SUBDIR_DONE, EXIT_STATUSES
from common.utils import *

# -----------------------------------------------------------------
#  Matplotlib settings
# -----------------------------------------------------------------
matplotlib.use('Agg')
usetex = matplotlib.checkdep_usetex(True)
matplotlib.rcParams['text.usetex'] = usetex

# TODO: add doc strings for these functions


def plot_run_space(parameters, N_sample, run_space, run_key, colormap=matplotlib.cm.viridis, output_dir='./',
                   file_type='png', show_plot=True):

    print('\nCreating parameter space vs run outcome visualisation')

    # PARAMETER_NUMBER_STELLAR_METALLICITY and PARAMETER_NUMBER_STELLAR_AGE
    N = PARAMETER_NUMBER

    # set up parameter ranges and labels
    p_labels = PARAMETER_NAMES_LATEX
    for i, label in enumerate(p_labels):
        p_labels[i] = label

    # Parameter names           Sampling intervals          Sampling units          Cloudy units
    # 1. Gas density            interval=[-3.0, 6.0]        log_10 (cm^-3)          same
    # 2. Gas phase metallicity  interval=[-3.0, 0.30103]    log_10( Z_solar)        10^()
    # 3. Redshift               interval=[3.0, 12.0]        Absolute value          same
    # 4. CR ionization factor   interval=[1.0, 3.0]         See Hazy X.y            10^()
    # 5. ionization parameter   interval=[-4.0, 0.0]        See Hazy 5.8            same
    # 6. Stellar metallicity    interval=[-5, -1.3979]      Absolute value          10^()
    # 7. Stellar age            interval=[1.0, 2000.0]      Myr                     ()*1e6
    # 8. DTM                    interval=[0., 0.5]          Absolute value          Not directly a cloudy parameter

    # parameters have the units used in Cloudy, here we change some of them to make the plots more accessible
    Z_gas_column = PARAMETER_NUMBER_GAS_PHASE_METALLICITY - 1
    t_star_column = PARAMETER_NUMBER_STELLAR_AGE - 1

    parameters[:, Z_gas_column] = np.log10(parameters[:, Z_gas_column])
    parameters[:, t_star_column] = parameters[:, t_star_column] / 1e6

    # parameter padding
    padding = [(-3.7, 6.7),
               (-3.2, 0.5),
               (2.0, 13.),
               (-100, 1100),
               (-4.4, 0.5),
               (-5.5, -1.1),
               (-200, 2200),
               (-0.1, 0.55)]

    # some plot settings
    marker_size = 20
    tick_label_size = 8
    label_size = 12

    # Some run space manipulation for separate plotting
    z = np.array(list(run_space.values())) # set parameter space color
    success = (z == 0)

    run_ticks = np.array(list(run_key.keys()))
    run_labels = np.array(list(run_key.values()))

    # set up main plot
    f, ax_array = plt.subplots(N, N, figsize=(14, 14))

    # choose a colormap
    c_m = colormap
    norm = matplotlib.colors.BoundaryNorm(np.arange(len(run_ticks)+1), c_m.N)

    for i in range(0, N):
        for j in range(0, N):

            # empty diagonals
            if i == j:
                ax_array[i, j].axis('off')

            # successful runs in the upper triangle
            elif j > i:

                ax = ax_array[i, j].scatter(x=parameters[:, j][success],
                                            y=parameters[:, i][success],
                                            c=z[success],
                                            s=marker_size,
                                            alpha=0.75,
                                            edgecolors='none',
                                            cmap=c_m,
                                            norm=norm
                                            )

                ax_array[i, j].set_ylim(padding[i])
                ax_array[i, j].set_xlim(padding[j])

                ax_array[i, j].grid(True, ls='dashed')
                ax_array[i, j].tick_params(axis='x', which='major', labelsize=tick_label_size, top=True, bottom=False)
                ax_array[i, j].tick_params(axis='y', which='major', labelsize=tick_label_size, right=True, left=False)

                if j == N-1:
                    ax_array[i, j].set_ylabel(ylabel=rF'${p_labels[i]}$', size=label_size, labelpad=10)
                    ax_array[i, j].yaxis.set_label_position('right')
                    ax_array[i, j].yaxis.set_tick_params(right='on', left='off')
                    ax_array[i, j].yaxis.set_ticks_position('right')
                if i == 0:
                    ax_array[i, j].set_xlabel(xlabel=rF'${p_labels[j]}$', size=label_size, labelpad=10)
                    ax_array[i, j].xaxis.set_label_position('top')
                    ax_array[i, j].xaxis.set_tick_params(top='on', bottom='off')
                    ax_array[i, j].xaxis.set_ticks_position('top')
                if j < N-1:
                    ax_array[i, j].set_yticklabels([])
                if i > 0:
                    ax_array[i, j].set_xticklabels([])

            # plotting the failed runs in the lower triangle
            elif j < i:

                ax = ax_array[i, j].scatter(x=parameters[:, j][~success],
                                            y=parameters[:, i][~success],
                                            c=z[~success],
                                            s=marker_size,
                                            alpha=0.75,
                                            edgecolors='none',
                                            cmap=c_m,
                                            norm=norm
                                            )

                ax_array[i, j].set_ylim(padding[i])
                ax_array[i, j].set_xlim(padding[j])

                ax_array[i, j].grid(True, ls='dashed')
                ax_array[i, j].tick_params(axis='x', which='major', labelsize=tick_label_size, top=False)
                ax_array[i, j].tick_params(axis='y', which='major', labelsize=tick_label_size, right=False)

                if i == N-1:
                    ax_array[i, j].set_xlabel(xlabel=rF'${p_labels[j]}$', size=label_size, labelpad=10)
                    ax_array[i, j].xaxis.set_label_position("bottom")
                    ax_array[i, j].xaxis.set_tick_params(top='off')
                if j == 0:
                    ax_array[i, j].set_ylabel(ylabel=rF'${p_labels[i]}$', size=label_size, labelpad=10)
                    ax_array[i, j].yaxis.set_label_position("left")
                    ax_array[i, j].yaxis.set_tick_params(right='off')
                if j > 0:
                    ax_array[i, j].set_yticklabels([])
                if i != N-1:
                    ax_array[i, j].set_xticklabels([])

    # make good use of space
    f.subplots_adjust(hspace=0, wspace=0, left=0.13, bottom=0.10, right=0.9, top=0.98)

    # make space for colorbar
    cbaxes = f.add_axes([0.96, 0.25, 0.02, 0.5])
    f.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=c_m), cax=cbaxes, orientation='vertical')
    cbaxes.set_yticks(run_ticks+0.5, fontsize=8)
    cbaxes.set_yticklabels(run_labels, fontsize=8)

    # build file name and save figure
    file_name = F'outcome_vs_p-space_sample_N{N_sample}.{file_type}'

    output_path = os.path.join(output_dir, file_name)

    f.savefig(output_path, bbox_inches='tight', dpi=300)

    print('Saved plot to: {}'.format(output_path))

    if show_plot:
        plt.show()
    else:
        plt.close()


def check_run(N_sample, colormap=matplotlib.cm.viridis, show_plot=True):

    # Location of parameter space files (assuming it exists)
    # TODO: these paths should probably not be hard-coded
    parameters = np.load(F'../data/samples/sample_N{N_sample}/parameters_N{N_sample}.npy')

    n_models_total = np.shape(parameters)[0]

    # File locations as an increasing list, again assuming it exists
    sample_dir = F'../data/samples/sample_N{N_sample}/{SAMPLE_SUBDIR_DONE}'
    model_dir_list = utils_get_model_folders(sample_dir)
    n_models_processed = len(model_dir_list)

    # Define dictionary to store summary statistics
    run_space = {}
    run_key = {0: 'Success',
               1: 'DNR',         # Did not run (could be because of scheduling)
               2: 'Empty',       # Cloudy problem with parameter space
               3: 'Abort',       # Cloudy aborted
               4: 'Wrong',       # Something went wrong
               5: 'Unphysical',  # Problem with parameter space or negative population
               6: 'Converge',    # Did not converge
               7: 'DNF'          # Did not finish in time (this is due to mine having allocated a fixed time to a run)
               }

    # Accounting array
    outcome_array = np.zeros(len(run_key))

    print(F"\nReading model outcomes for all models in {sample_dir}")

    for i in tqdm(range(len(model_dir_list))):

        # Get the tail of the cloudy output file
        tail = utils_read_model_output_tail(model_dir_list[i])

        if "Cloudy exited OK" in tail:
            run_space[i] = 0
            outcome_array[0] += 1
        elif tail == 0:
            run_space[i] = 1
            outcome_array[1] += 1
        elif tail == '':
            run_space[i] = 2
            outcome_array[2] += 1
        elif 'ABORT' in tail:
            run_space[i] = 3
            outcome_array[3] += 1
        elif 'something went wrong' in tail:
            run_space[i] = 4
            outcome_array[4] += 1
        elif 'unphysical' in tail or 'negative population' in tail:
            run_space[i] = 5
            outcome_array[5] += 1
        elif 'did not converge' in tail:
            run_space[i] = 6
            outcome_array[6] += 1
        elif "Cloudy exited OK" not in tail:
            run_space[i] = 7
            outcome_array[7] += 1

    print(F"\n{n_models_total} models in total in this sample")
    print(F"{n_models_processed} models processed ({np.round(100 * n_models_processed/n_models_total, 2)}%)")
    print(F"Breakdown of the EXIT codes:\n")
    for i in range(len(run_key)):
        outcome_percent = np.round(100 * outcome_array[i] / n_models_processed, 2)
        print(F"\t{outcome_percent}% \t|\t{i}: {run_key[i]} ")

    if n_models_processed == n_models_total:
        plot_run_space(parameters, N_sample, run_space, run_key, colormap=colormap, show_plot=show_plot)


if __name__ == "__main__":

    # type in `python3 check_runs.py --N_sample 8000`

    parser = argparse.ArgumentParser()
    parser.add_argument("--N_sample", required=True, type=int,
                        help="Number of models in the sample. ")

    args = parser.parse_args()
    check_run(args.N_sample, show_plot=False)
