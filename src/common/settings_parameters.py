# Settings related to the parameters and their ranges can go in here

# -----------------------------------------------------------------
#  Settings for data sets with 5 parameters
# -----------------------------------------------------------------

PARAMETER_NUMBER = 5

# Parameter names           Intervals                   Units
# 1. Gas density            interval=[-3.0, 6.0]        log (cm^-3)
# 2. Gas phase metallicity  interval=[0.01, 2.0]        Solar metallicity
# 2. Redshift               interval=[3.0, 12.0]        Absolute value
# 4. Stellar metallicity    interval=[1e-5, 0.04]       Absolute value
# 5. Stellar age            interval=[1.0, 2000.0]      Myr

PARAMETER_LIMITS = [[-3.0, 6.0],
                    [0.01, 3.0],
                    [3.0, 12.0],
                    [1e-5, 0.04],
                    [1.0, 2000.0]
                    ]

PARAMETER_NUMBER_REDSHIFT = 3
PARAMETER_NUMBER_STELLAR_AGE = 5

# LaTeX names of our parameters (for matplotlib)
PARAMETER_NAMES_LATEX =['\log_{10}(\\rho\, \mathrm{cm^{3}})',
                        'Z/Z_{\\odot}',
                        'z',
                        'Z_{\\ast}',
                        't_{\\ast}'
                        ]


