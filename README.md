## pyNublado

Docs: https://raulorteg.github.io/pyNublado/

A package to run (a lot of) [Cloudy](https://nublado.org) models.

### Running Cloudy

Example of running Cloudy independently:
1. Create a _[name].in_ file
2. Navigate to the folder where the .in file is located
3. Execute Cloudy from the directory ```~/c17.02/source/cloudy.exe [name].in```


### Input parameters
* Gas density (log scale): -3 - 6
* Gas phase metallicity: 0.0001 - 2.0 (solar) 
* CMB background (z_redshift): 3-12
* Cosmic rays background: ```cosmic rays background linear 1``` 1-1000
* Ionization parameter: -4 - 0 (log units)
* Radiation spectrum (BPASS), Chabrier IMF, Mup=300 M_sun: depends on age, metallicity (Z)
    * Stellar ages (is delimited by the redshift): 1 Myr up to 2 Gyr.
    * Stellar metallicity (Z): 1e-5-0.040 (absolute value)


### Output params:
* Lines in ```data/LineLabels_filtered.txt```.

