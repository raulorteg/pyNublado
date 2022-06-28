# pyNublado

A Python package to run (a lot of) [Cloudy](https://nublado.org) models.


## Documentation
Information pertaining to the installation, usage, available parameters, and science can be found in the [documentation](https://raulorteg.github.io/pyNublado/)

## Cite this repo / work
Add paper reference here once it is ready.

## Feedback
Feedback and questions are welcome. Please get in touch.



=======
Example of running Cloudy independently:
1. Create a _[name].in_ file
2. Navigate to the folder where the .in file is located
3. Execute Cloudy from the directory ```~/c17.03/source/cloudy.exe [name].in```


### Input parameters
* Gas density (log scale): -3 - 6
* Gas phase metallicity: 0.0001 - 2.0 (solar)
* CMB background (z_redshift): 3-12
* Cosmic rays background: ```cosmic rays background linear 1``` 1-1000
* Ionization parameter: -4 - 0 (log units)
* DTM: dust to metal ratio 0-0.5
* Radiation spectrum (BPASS), Chabrier IMF, Mup=300 M_sun: depends on age, metallicity (Z)
    * Stellar ages (is delimited by the redshift): 1 Myr up to 2 Gyr.
    * Stellar metallicity (Z): 1e-5-0.040 (absolute value)





### Testing
Tests can be found in ```tests/```, to run the tests with pytest:
1. Install pytest ```pip install pytest```
2. Navigate to tests ```cd tests```
3. Run tests ```pytest -v test.py```, the -v flag is optional for verbosity

The tests check if cloudy path in ```src/common/settings.py``` is the correct path of the cloudy installation in our system by runnning a test model.in, then checks if the output of CLOUDY is ok ("Cloudy exited OK"), then creates the file structure src.manager.QueueManager() expects and runs 4 models on multiple cpus to check the pipeline.
