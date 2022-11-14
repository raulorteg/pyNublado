# Global settings can go in here

RANDOM_SEED = 42

SAMPLE_DIR_BASE = 'sample_N'
SAMPLE_SUBDIR_TODO = 'todo'
SAMPLE_SUBDIR_DONE = 'done'

PARAMETER_FILE_BASE = 'parameters_N'
CLOUDY_IN_FILE = 'model.in'

INPUT_PARAMETER_NAMES = ["gas_density",
                         "gas_phase_metallicity",
                         "redshift",
                         "cr_ionization_factor",
                         "ionization_parameter",
                         "stellar_metallicity",
                         "stellar_age",
                         "dtm"]

EXIT_STATUSES_INT = {
                0: 'Success',
                1: 'DNR',         # Did not run (could be because of scheduling)
                2: 'Empty',       # Cloudy problem with parameter space
                3: 'Abort',       # Cloudy aborted
                4: 'Wrong',       # Something went wrong
                5: 'Unphysical',  # Problem with parameter space or negative population
                6: 'Converge',    # Did not converge
                7: 'DNF'          # Did not finish in time (this is due to mine having allocated a fixed time to a run)
                }

EXIT_STATUSES = {
            'Success':0,
            'DNR':1,         # Did not run (could be because of scheduling)
            'Empty':2,       # Cloudy problem with parameter space
            'Abort':3,       # Cloudy aborted
            'Wrong':4,       # Something went wrong
            'Unphysical':5,  # Problem with parameter space or negative population
            'Converge':6,    # Did not converge
            'DNF':7          # Did not finish in time (this is due to mine having allocated a fixed time to a run)
            }
