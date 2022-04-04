from datetime import datetime
import sys; sys.path.append('..')
import glob, os.path, re


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


def utils_get_current_timestamp():
    """
    Get a current time stamp

    Returns:
        Custom formatted date time string
    """
    return datetime.now().strftime('%Y_%m_%d__%H_%M_%S')


def atoi(text):
    """
    Args:
        text: Input string
    Returns:
        Converts 'text' to integer if it is a digit
    """
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    Splits text to its digit
    Args:
        text: Input string
    Returns:
        Integer portion of text if it contains digits
    """

    return [atoi(c) for c in re.split('(\d+)', text)]


def get_folders(target_dir):
    """
    Get folders in 'target_dir'
    Args:
        target_dir: A string containing the target directory of samples
    Returns:
        List of folders
    """

    folders = glob.glob(traget_dir+'*/', recursive = True)
    folders.sort(key=natural_keys)

    return folders

def read_output(folder_name):
    """
    Reads in 'model.out' inside 'folder_name'
    Args:
        folder_name: A string containing a sample directory with cloudy outputs
    Returns:
        A string with the last 3 lines of output, returns '' if empty
    """

    with open(F'{folder_name}model.out', 'r') as f:
        last_line = f.readlines()[-3:]

    last_line=''.join(last_line)
    last_line=re.sub(r'[\n]|\[|\]', '', last_line)

    return last_line
