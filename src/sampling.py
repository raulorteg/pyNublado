import os
import numpy as np
from pyDOE import *

from common.settings_parameters import PARAMETER_NUMBER, PARAMETER_LIMITS
from common.settings import PARAMETER_FILE
from common.utils import *


def sampling_create_parameters(path, prefix, n_samples, filter=False, save_to_file=True):
    """
    This function creates a set of parameters for a sample.

    Args:
        path: output directory
        prefix: file prefix
        n_samples: Number of parameter samples to be generated
        save_to_file: Save parameters to file
        filter: Filter the sample for parameter combinations that are unphysical.
                This will results in a lower n_sample than specified.

    Returns:
          A 2D numpy array in which each row represents a parameter vector.
          It will also be saved as a numpy object.
    """

    if not os.path.exists(path):
        os.makedirs(path)
        print('Created directory {}'.format(path))

    # get normalised latin hyper cube (all parameter values are in the [0,1] range)
    lhs_normalised = lhs(n=PARAMETER_NUMBER, samples=n_samples)

    parameters = utils_rescale_parameters(limits=PARAMETER_LIMITS, parameters=lhs_normalised)

    if filter:
        print('Filtering unphysical parameter combinations')
        parameters = sampling_filter_redshift_stellar_age(parameters)

    if save_to_file:
        file_name = '{}_{}_N{}.npy'.format(prefix, PARAMETER_FILE, n_samples)
        parameter_file_path = os.path.join(path, file_name)
        np.save(parameter_file_path, parameters)
        print('Saved parameter file to {}'.format(parameter_file_path))

    return parameters


def sampling_filter_redshift_stellar_age(parameters):

    # tba.

    return parameters


# -----------------------------------------------------------------
# execute this when file is executed
# -----------------------------------------------------------------
if __name__ == "__main__":

    target_directory = '../data/samples/'
    target_prefix = 'test_sample'
    N = 1000

    sampling_create_parameters(path=target_directory,
                               prefix=target_prefix,
                               n_samples=N,
                               filter=False,
                               save_to_file=True
                               )


