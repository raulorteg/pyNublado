# -----------------------------------------------------------------
#  Settings for data sets with 8 parameters
# -----------------------------------------------------------------

PARAMETER_NUMBER = 8

# Parameter names           Sampling intervals          Sampling units          Cloudy units
# 1. Gas density            interval=[-3.0, 6.0]        log_10 (cm^-3)          same
# 2. Gas phase metallicity  interval=[-3.0, 0.30103]    log_10( Z_solar)        10^()
# 3. Redshift               interval=[3.0, 12.0]        Absolute value          same
# 4. CR ionization factor   interval=[1.0, 3.0]         See Hazy X.y            10^()
# 5. ionization parameter   interval=[-4.0, 0.0]        See Hazy 5.8            same
# 6. Stellar metallicity    interval=[-5, -1.3979]      Absolute value          10^()
# 7. Stellar age            interval=[1.0, 2000.0]      Myr                     ()*1e6
# 8. DTM                    interval=[0., 0.5]          Absolute value          Not directly a cloudy parameter

PARAMETER_LIMITS = [[-3.0, 6.0],
                    [-3.0, 0.30103],
                    [3.0, 12.0],
                    [1.0, 3.0],
                    [-4.0, 0.0],
                    [-5.0, -1.3979],
                    [1.0, 2000.0],
                    [0., 0.5]
                    ]

PARAMETER_NUMBER_GAS_PHASE_METALLICITY = 2
PARAMETER_NUMBER_REDSHIFT = 3
PARAMETER_NUMBER_CR_SCALING = 4
PARAMETER_NUMBER_STELLAR_METALLICITY = 6
PARAMETER_NUMBER_STELLAR_AGE = 7
PARAMETER_NUMBER_DTM = 8

# LaTeX names of our parameters (for matplotlib)
PARAMETER_NAMES_LATEX =['\mathrm{log}_{10}(n_{\mathrm{gas}} / \mathrm{cm^{-3}})',
                        '\mathrm{log}_{10}(Z_{\mathrm{gas}} / Z_{\odot})',
                        'z',
                        '\mathrm{CR\, scaling}',
                        '\mathrm{log}_{10}(U)',
                        '\mathrm{log}_{10}(Z_{\star})',
                        't_{\star} / \mathrm{Myr}',
                        '\mathrm{DTM\, ratio}'
                        ]
