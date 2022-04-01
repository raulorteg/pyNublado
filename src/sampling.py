import os
import numpy as np
from pyDOE import *
import astropy.units as u
from astropy.cosmology import Planck18


from common.settings_parameters import *
from common.settings import PARAMETER_FILE_BASE, RANDOM_SEED, SAMPLE_DIR_BASE
from common.utils import *
from common.plot import *


def sampling_create_parameters(path, n_samples, filter=False, save_to_file=True, plot=False):
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

    folder = '{}{}'.format(SAMPLE_DIR_BASE, n_samples)
    path = os.path.join(path, folder)

    if not os.path.exists(path):
        os.makedirs(path)
        print('Created directory {}'.format(path))

    np.random.seed(RANDOM_SEED)

    # get normalised latin hyper cube (all parameter values are in the [0,1] range)
    lhs_normalised = lhs(n=PARAMETER_NUMBER, samples=n_samples)

    parameters = utils_rescale_parameters(limits=PARAMETER_LIMITS, parameters=lhs_normalised)

    if filter:
        parameters = sampling_filter_redshift_stellar_age(parameters)

    if plot:
        plot_parameter_space(parameters=parameters, n_samples=n_samples, output_dir=path, file_type='png')

    parameters = sampling_adjust_columns(parameters)

    if save_to_file:

        file_name = '{}_N{}.npy'.format(PARAMETER_FILE_BASE, n_samples)

        parameter_file_path = os.path.join(path, file_name)
        np.save(parameter_file_path, parameters)
        print('Saved parameter file to {}'.format(parameter_file_path))

    return parameters


def sampling_adjust_columns(parameters):
    """
    Metalicities are sampled in log space and have to be changed to linear space.
    Cloudy wants the stellar age in years and not Mega years.

    Args:
        parameters: parameter object

    Returns: parameter objact

    """

    Z_gas_column = PARAMETER_NUMBER_GAS_PHASE_METALLICITY - 1
    Z_star_column = PARAMETER_NUMBER_STELLAR_METALLICITY - 1
    t_star_column = PARAMETER_NUMBER_STELLAR_AGE - 1

    parameters[:, Z_gas_column] = 10 ** (parameters[:, Z_gas_column])
    # parameters[:, Z_star_column] = 10 ** (parameters[:, Z_star_column])
    parameters[:, t_star_column] = 1e6 * parameters[:, t_star_column]

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

    N = 2000

    sampling_create_parameters(path=target_directory,
                               n_samples=N,
                               filter=True,
                               save_to_file=True,
                               plot=True
                               )
