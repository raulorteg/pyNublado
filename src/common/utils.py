from datetime import datetime
import sys; sys.path.append('..')


# -----------------------------------------------------------------
# functions to scale and re-scale parameters
# -----------------------------------------------------------------
# scale all parameters to [0,1]
def utils_scale_parameters(limits, parameters):

    for i in range(parameters.shape[1]):

        a = limits[i][0]
        b = limits[i][1]

        parameters[:, i] = (parameters[:, i] - a) / (b - a)

    return parameters


# re-scale all parameters to original limits
def utils_rescale_parameters(limits, parameters):

    for i in range(parameters.shape[1]):

        a = limits[i][0]
        b = limits[i][1]

        parameters[:, i] = parameters[:, i] * (b - a) + a

    return parameters


# re-scale a single given parameter
def utils_rescale_parameters_single(limits, p):

    for i in range(0, len(p)):

        a = limits[i][0]
        b = limits[i][1]

        p[i] = p[i] * (b - a) + a

    return p


# -----------------------------------------------------------------
# Current time stamp as a string
# -----------------------------------------------------------------
def utils_get_current_timestamp():

    return datetime.now().strftime('%Y_%m_%d__%H_%M_%S')