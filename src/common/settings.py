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

EXIT_STATUSES = {"successful": 0,
                 "aborted": 1,
                 "unfinished": 2,
                 "empty": 3,
                 "not_exists": 4}






