import glob
import os.path
import re
from datetime import datetime

import sys; sys.path.append('..')
from common.settings import *


def utils_scale_parameters(limits, parameters):
    """
    This function scales a set of parameters of a given range (defined by limits) to the range [0,1]

    Args:
        limits: A 2D list or array defining the limits of the parameter object
        parameters: A 2D list or array of parameters in the limits given by 'limits'
    Returns:
        The parameter 2D object scaled to [0,1]
    """

    for i in range(parameters.shape[1]):

        a = limits[i][0]
        b = limits[i][1]

        parameters[:, i] = (parameters[:, i] - a) / (b - a)

    return parameters


def utils_rescale_parameters(limits, parameters):
    """
    This function re-scales a set of parameters in the range [0,1] to a given range defined by limits

    Args:
        limits: A 2D list or array of limits to re-scale to
        parameters: A 2D list or array of parameters in the range [0,1]
    Returns:
        The re-scaled 1D parameter object
    """

    for i in range(parameters.shape[1]):

        a = limits[i][0]
        b = limits[i][1]

        parameters[:, i] = parameters[:, i] * (b - a) + a

    return parameters


def utils_rescale_parameters_single(limits, p):
    """
    This function re-scales a given parameter vector in the range [0,1] to a range defined by 'limits'

    Args:
        limits: A 2D list or array of limits to re-scale to
        p: A parameter vector gives as 1D list or array
    Returns:
        The re-scaled 1D parameter object
    """

    for i in range(0, len(p)):

        a = limits[i][0]
        b = limits[i][1]

        p[i] = p[i] * (b - a) + a

    return p


def utils_setup_sample_dir(parent_path, N_sample):
    """
    Create the sample directory and its sub directories if they do not yet exist.
    If the directory exists, do not overwrite anything.

    Args:
        parent_path: string: parent path
        N_sample:  int: number of samples

    Returns: string: containing the sample path
             boolean: False if the directory already exists, True otherwise
    """

    folder = '{}{}'.format(SAMPLE_DIR_BASE, N_sample)
    path = os.path.join(parent_path, folder)

    new_directory = not os.path.isdir(path)

    if new_directory:
        os.makedirs(path)
        print('Created directory {}'.format(path))

        path_todo = os.path.join(path, SAMPLE_SUBDIR_TODO)
        path_done = os.path.join(path, SAMPLE_SUBDIR_DONE)

        os.makedirs(path_todo)
        os.makedirs(path_done)

        print('Created directory {}'.format(path_todo))
        print('Created directory {}'.format(path_done))

    return path, new_directory


def utils_get_current_timestamp():
    """
    Get a current time stamp

    Returns:
        Custom formatted date time string
    """
    return datetime.now().strftime('%Y_%m_%d__%H_%M_%S')


def utils_atoi(text):
    """
    Args:
        text: Input string
    Returns:
        Converts 'text' to integer if it is a digit
    """
    return int(text) if text.isdigit() else text


def utils_natural_keys(text):
    """
    Splits text to its digit
    Args:
        text: Input string
    Returns:
        Integer portion of text if it contains digits
    """

    return [utils_atoi(c) for c in re.split('(\d+)', text)]


def utils_get_model_folders(target_dir):
    """
    Get a list of model folders in 'target_dir'
    Args:
        target_dir: A string containing the target directory of samples
    Returns:
        List of folders
    """

    folders = glob.glob(target_dir+'/*', recursive=True)
    folders.sort(key=utils_natural_keys)

    return folders


def utils_read_model_output_tail(folder_name, tail_len=5):
    """
    Reads in the tail strings of 'model.out' inside 'folder_name'
    Args:
        folder_name: A string containing a sample directory with cloudy outputs
        tail_len: Number of tail strings to read in
    Returns:
        A string with the last 'tail_len' lines of output, returns 0 if file not found
    """

    try:
        with open(F'{folder_name}/model.out', 'r') as f:
            tail = f.readlines()[-tail_len:]

        tail = ''.join(tail)
        # Remove all newline (\n) and square brackets
        tail = re.sub(r'[\n]|\[|\]', '', tail)
    except FileNotFoundError:
        tail = 0

    return tail
