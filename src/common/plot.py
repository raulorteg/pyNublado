import os
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc

import sys; sys.path.append('..')
from common.settings_parameters import *


# -----------------------------------------------------------------
#  Matplotlib settings
# -----------------------------------------------------------------
matplotlib.use('Agg')
usetex = matplotlib.checkdep_usetex(True)
mpl.rc('text', usetex=usetex)


# -----------------------------------------------------------------
#  visualise the sample distribution of the whole parameter space
# -----------------------------------------------------------------
def plot_parameter_space(parameters, N_sample, output_dir, file_type='png'):

    print('Creating parameter space visualisation')

    N = PARAMETER_NUMBER

    # set up parameter ranges and labels
    p_labels = PARAMETER_NAMES_LATEX
    for i, label in enumerate(p_labels):
        p_labels[i] = '$' + label + '$'

    # In general our parameters have the units as used in Cloudy.
    # For this plot we change some of them to make the sub-plots more accessible

    # Parameter names           Sampling intervals          Sampling units          Cloudy units
    # 1. Gas density            interval=[-3.0, 6.0]        log_10 (cm^-3)          same
    # 2. Gas phase metallicity  interval=[-3.0, 0.30103]    log_10( Z_solar)        10^()
    # 3. Redshift               interval=[3.0, 12.0]        Absolute value          same
    # 4. CR ionization factor   interval=[1.0, 3.0]         See Hazy X.y            10^()
    # 5. ionization parameter   interval=[-4.0, 0.0]        See Hazy 5.8            same
    # 6. Stellar metallicity    interval=[-5, -1.3979]      Absolute value          10^()
    # 7. Stellar age            interval=[1.0, 2000.0]      Myr                     ()*1e6
    # 8. DTM                    interval=[0., 0.5]          Absolute value          Not directly a cloudy parameter

    Z_gas_column = PARAMETER_NUMBER_GAS_PHASE_METALLICITY - 1
    t_star_column = PARAMETER_NUMBER_STELLAR_AGE - 1

    parameters[:, Z_gas_column] = np.log10(parameters[:, Z_gas_column])
    parameters[:, t_star_column] = parameters[:, t_star_column] / 1e6

    # parameter padding
    padding = [(-3.7, 6.7), (-3.2, 0.5), (2.0, 13.), (-100, 1100), (-4.4, 0.5), (-5.5, -1.1), (-200, 2200), (-0.1, 0.55)]

    # some plot settings
    marker_size = 100
    tick_label_size = 18
    label_size = 18

    # set up main plot
    f, ax_array = plt.subplots(N - 1, N - 1, figsize=(14, 14))
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

    # build file name and save figure

    file_name = 'parameter_space_N{}.{}'.format(N_sample, file_type)

    output_path = os.path.join(output_dir, file_name)
    f.savefig(output_path)

    print('  Saved plot to: {} '.format(output_path))
