import os
import numpy as np
from pyDOE import *
import astropy.units as u
from astropy.cosmology import Planck18


from common.settings_parameters import *
from common.settings import PARAMETER_FILE
from common.utils import *
from common.plot import *


def sampling_create_parameters(path, prefix, n_samples, filter=False, save_to_file=True, plot=False):
    """
    This function creates a set of parameters for a sample.

    Args:
        path: output directory
        prefix: file prefix
        n_samples: Number of parameter samples to be generated
        save_to_file: Boolean - Save parameters to file
        filter: Boolean - Filter the sample for parameter combinations that are unphysical.
                          This will results in a lower n_sample than specified.
        plot: Boolean - create a visualisation of the parameter space

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
        parameters = sampling_filter_redshift_stellar_age(parameters)
        n_samples = parameters.shape[0]

    if save_to_file:
        if prefix:
            file_name = '{}_{}_N{}.npy'.format(prefix, PARAMETER_FILE, n_samples)
        else:
            file_name = '{}_N{}.npy'.format(PARAMETER_FILE, n_samples)

        parameter_file_path = os.path.join(path, file_name)
        np.save(parameter_file_path, parameters)
        print('Saved parameter file to {}'.format(parameter_file_path))

    if plot:
        plot_parameter_space(parameters=parameters, output_dir=path, prefix=prefix, file_type='png')

    return parameters


def sampling_filter_redshift_stellar_age(parameters):
    """
    Remove all parameter vectors for which the stellar age exceeds the age of the universe (given by the redshift)

    Args:
        parameters: 2D array containing the parameters

    Returns:
        The filtered 2D parameter array
    """

    print('Filtering un-physical parameter combinations:')

    n_samples_pre = parameters.shape[0]

    z_column = PARAMETER_NUMBER_REDSHIFT - 1
    t_column = PARAMETER_NUMBER_STELLAR_AGE - 1

    redshifts = parameters[:, z_column]
    stellar_ages = parameters[:, t_column]

    # convert redshifts to ages
    cosmology = Planck18
    redshift_ages = cosmology.age(z=redshifts).to_value(u.Myr)

    # create and apply mask (indexes True will be kept)
    mask = redshift_ages > stellar_ages
    parameters = parameters[mask]

    # bookkeeping
    n_samples_post = parameters.shape[0]
    delta = n_samples_pre - n_samples_post
    print('  {} samples removed. {} remaining.'.format(delta, n_samples_post))

    return parameters


# -----------------------------------------------------------------
# execute this when file is executed
# -----------------------------------------------------------------
if __name__ == "__main__":

    target_directory = '../data/samples/'
    target_prefix = 'test_filter'
    N = 2000

    sampling_create_parameters(path=target_directory,
                               prefix=target_prefix,
                               n_samples=N,
                               filter=True,
                               save_to_file=True,
                               plot=False
                               )
