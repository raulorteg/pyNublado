# Parameters

pyNublado is set up to employ eight different input parameters for Cloudy runs. The parameters and their respective ranges are given below.


### Cloudy input parameters
1. Gas density (log scale): -3 - 6
2. Gas phase metallicity: 0.0001 - 2.0 (solar) 
3. CMB background (z_redshift): 3 - 12
4. Cosmic rays background: ```cosmic rays background linear 1``` 1 - 1000
5. Ionization parameter: -4 - 0 (log units)
6. Stellar ages (is delimited by the redshift): 1 Myr up to 2 Gyr.
7. Stellar metallicity (Z): 1e-5 - 0.040 (absolute value)
8. Dust to metal ratio:     0.0 - 0.5
    
For the radiation spectra of our sources we use the BPASS model (Chabrier IMF, Mup=300 M_sun), which depends on stellar age (parameter 6) and stellar metallicity (parameter 7).

A Not on the dust to metal parameter: (Aswin?)


Parameter ranges can be altered in ```src/common/settings_parameters.py```


### Output parameters

The list of emission lines that the Cloudy runs will output is defined and can be altered in the following file: ```data/LineList_in.txt```.