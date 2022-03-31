import os
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc

import sys; sys.path.append('..')
from common.settings_parameters import PARAMETER_LIMITS, PARAMETER_NAMES_LATEX, PARAMETER_NUMBER


# -----------------------------------------------------------------
#  Matplotlib settings
# -----------------------------------------------------------------
matplotlib.use('Agg')
mpl.rc('text', usetex=True)


# -----------------------------------------------------------------
#  visualise the sample distribution of the whole parameter space
# -----------------------------------------------------------------
def plot_parameter_space(parameters, output_dir, prefix, file_type='png'):

    print('Creating parameter space visualisation')

    N = PARAMETER_NUMBER

    n_samples = parameters.shape[0]

    # set up parameter ranges and labels
    p_labels = PARAMETER_NAMES_LATEX
    for i, label in enumerate(p_labels):
        p_labels[i] = '$' + label + '$'

    # parameter ranges and padding
    # 1. Gas density            interval=[-3.0, 6.0]        log (cm^-3)
    # 2. Gas phase metallicity  interval=[0.01, 2.0]        Solar metallicity
    # 2. Redshift               interval=[3.0, 12.0]        Absolute value
    # 4. Stellar metallicity    interval=[1e-5, 0.04]       Absolute value
    # 5. Stellar age            interval=[1.0, 2000.0]      Myr

    padding = [(-3.5, 6.5), (-0.2, 2.2), (2.0, 13.), (1e-5, 0.043), (-150, 2080)]

    # some plot settings
    marker_size = 150
    tick_label_size = 20
    label_size = 26

    # set up main plot
    f, ax_array = plt.subplots(N - 1, N - 1, figsize=(12, 12))
    for i in range(0, N - 1):
        for j in range(1, N):
            if j > i:

                ax = ax_array[N - 2 - i, j - 1].scatter(x=parameters[:, j],
                                                        y=parameters[:, i],
                                                        marker='h',
                                                        s=marker_size,
                                                        alpha=0.75,
                                                        edgecolors='none',
                                                        cmap=mpl.cm.inferno_r
                                                        )
                ax_array[N - 2 - i, j - 1].set_ylim(padding[i])
                ax_array[N - 2 - i, j - 1].set_xlim(padding[j])

                if i == 0:
                    # bottom row
                    ax_array[N - 2 - i, j - 1].tick_params(axis='x', which='major', labelsize=tick_label_size)
                    ax_array[N - 2 - i, j - 1].set_xlabel(xlabel=r'$\textrm{%s}$' % p_labels[j], size=label_size, labelpad=10)

                    if i != j - 1:
                        # turn of labels and ticks on all panels except the leftmost panel
                        ax_array[N - 2 - i, j - 1].tick_params(axis='y', which='both', length=0.)
                        ax_array[N - 2 - i, j - 1].axes.yaxis.set_ticklabels([])

                if i == j - 1:
                    # leftmost panel in each row
                    ax_array[N - 2 - i, j - 1].tick_params(axis='y', which='major', labelsize=tick_label_size)
                    ax_array[N - 2 - i, j - 1].set_ylabel(ylabel=r'$\textrm{%s}$' % p_labels[i], size=label_size, labelpad=10)

                    if i != 0:
                        ax_array[N - 2 - i, j - 1].tick_params(axis='x', which='both', length=0.)
                        ax_array[N - 2 - i, j - 1].axes.xaxis.set_ticklabels([])

                if (i != 0) and (i != j - 1):
                    # turn of labels & ticks for all panels not in the bottom row and not leftmost
                    ax_array[N - 2 - i, j - 1].tick_params(axis='y', which='both', length=0.)
                    ax_array[N - 2 - i, j - 1].tick_params(axis='x', which='both', length=0.)
                    ax_array[N - 2 - i, j - 1].axes.yaxis.set_ticklabels([])
                    ax_array[N - 2 - i, j - 1].axes.xaxis.set_ticklabels([])

                ax_array[N - 2 - i, j - 1].set_aspect('auto')

            else:
                # do not draw the panels above the diagonal
                ax_array[N - 2 - i, j - 1].axis('off')

    # make good use of space
    f.subplots_adjust(hspace=0, wspace=0, left=0.13, bottom=0.10, right=0.95, top=0.98)

    # build file name

    if prefix:
        file_name = '{}_parameter_space_N{}.{}'.format(prefix, n_samples, file_type)

    else:
        file_name = 'parameter_space_N{}.{}'.format(n_samples, file_type)

    output_path = os.path.join(output_dir, file_name)
    f.savefig(output_path)

    print('  Saved plot to: {} '.format(output_path))
