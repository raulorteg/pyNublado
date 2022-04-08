import numpy as np
from pyDOE import *
import astropy.units as u
from astropy.cosmology import Planck18


from common.settings_parameters import *
from common.settings import PARAMETER_FILE_BASE, RANDOM_SEED, SAMPLE_DIR_BASE
from common.utils import *
from common.plot import *


def sampling_create_parameters(path, N_sample, filter=False, save_to_file=True, plot=False):
    """
    This function creates a set of parameters for a sample.

    :param str path: output directory
    :param int N_sample: Number of parameter samples to be generated
    :param bool save_to_file: Boolean - Save parameters to file
    :param bool filter: Boolean - Filter the sample for parameter combinations that are unphysical.
    This will results in a lower n_sample than specified.
    :param bool plot: Boolean - create a visualisation of the parameter space

    :return: A 2D numpy array in which each row represents a parameter vector. It will also be saved as a numpy object.
    :rtype: numpy.array
    """

    print('Creating a set of parameters (N = {}) '.format(N_sample))

    np.random.seed(RANDOM_SEED)

    # get normalised latin hyper cube (all parameter values are in the [0,1] range)
    lhs_normalised = lhs(n=PARAMETER_NUMBER, samples=N_sample)

    parameters = utils_rescale_parameters(limits=PARAMETER_LIMITS, parameters=lhs_normalised)

    if filter:
        parameters = sampling_filter_redshift_stellar_age(parameters)

    # transform some column from the sampling ranges to the units that Cloudy requires
    parameters = sampling_adjust_units(parameters)

    if plot:
        plot_parameter_space(parameters=parameters, N_sample=N_sample, output_dir=path, file_type='png')

    if save_to_file:

        file_name = '{}{}.npy'.format(PARAMETER_FILE_BASE, N_sample)

        parameter_file_path = os.path.join(path, file_name)
        np.save(parameter_file_path, parameters)
        print('Saved parameter file to {}'.format(parameter_file_path))

    return parameters


def sampling_adjust_units(parameters):
    """
    Some parameter units have to be adjusted to be compatible with Cloudy's input formats.

    For example, we sampled some parameters in log space which need to be changed to linear space.
    Others parameters might require linear transformations.

    All required changes can be performed in this function.

    :param parameters: parameter object
    :return: parameter object
    """
    print('  Adjusting sampling units')

    Z_gas_column = PARAMETER_NUMBER_GAS_PHASE_METALLICITY - 1
    cr_column = PARAMETER_NUMBER_CR_SCALING - 1
    t_star_column = PARAMETER_NUMBER_STELLAR_AGE - 1

    parameters[:, Z_gas_column] = 10 ** (parameters[:, Z_gas_column])
    parameters[:, cr_column] = 10 ** (parameters[:, cr_column])

    parameters[:, t_star_column] = 1e6 * parameters[:, t_star_column]

    return parameters


def sampling_filter_redshift_stellar_age(parameters):
    """
    Remove all parameter vectors for which the stellar age exceeds the age of the universe (given by the redshift)

    :param numpy.array parameters: 2D array containing the parameters
    :return: The filtered 2D parameter array
    :rtype: numpy.array
    """

    print('  Filtering un-physical parameter combinations')

    N_sample_pre = parameters.shape[0]

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
    N_sample_post = parameters.shape[0]
    delta = N_sample_pre - N_sample_post
    print('  {} samples removed. {} remaining.'.format(delta, N_sample_post))

    return parameters


# -----------------------------------------------------------------
# Testing ... 1, 2, 3
# -----------------------------------------------------------------
if __name__ == "__main__":

    sample_directory = '../data/samples/test_sample_N2000'

    if not os.path.isdir(sample_directory):
        os.makedirs(sample_directory)

    N = 2000

    sampling_create_parameters(path=sample_directory,
                               N_sample=N,
                               filter=True,
                               save_to_file=True,
                               plot=True
                               )
