# -----------------------------------------------------------------
#  Settings for data sets with 7 parameters
# -----------------------------------------------------------------

PARAMETER_NUMBER = 7

# Parameter names           Intervals                   Units
# 1. Gas density            interval=[-3.0, 6.0]        log_10 (cm^-3)
# 2. Gas phase metallicity  interval=[-3.0, 0.30103]    Solar metallicity
# 3. Redshift               interval=[3.0, 12.0]        Absolute value
# 4. CR ionization factor   interval=[1.0, 3.0]         log_10 of Cosmic ray scaling factor, see Hazy X.y
# 5. ionization parameter   interval=[-4.0, 0.0]        See Hazy 5.8
# 6. Stellar metallicity    interval=[-5, -1.3979]      Absolute value
# 7. Stellar age            interval=[1.0, 2000.0]      Myr

PARAMETER_LIMITS = [[-3.0, 6.0],
                    [-3.0, 0.30103],
                    [3.0, 12.0],
                    [1.0, 3.0],
                    [-4.0, 0.0],
                    [-5.0, -1.3979],
                    [1.0, 2000.0]
                    ]

PARAMETER_NUMBER_GAS_PHASE_METALLICITY = 2
PARAMETER_NUMBER_REDSHIFT = 3
PARAMETER_NUMBER_CR_SCALING = 4
PARAMETER_NUMBER_STELLAR_METALLICITY = 6
PARAMETER_NUMBER_STELLAR_AGE = 7

# LaTeX names of our parameters (for matplotlib)
PARAMETER_NAMES_LATEX =['\log_{10}(\\rho_{\mathrm{gas}} \, \mathrm{cm^{3}})',
                        '\log_{10}(Z_{\mathrm{gas}}/Z_{\\odot})',
                        'z',
                        '\mathrm{CR\, scaling}',
                        '\mathrm{U}',
                        '\log_{10}(Z_{\\ast})',
                        't_{\\ast} \; [Myr]'
                        ]


