# pyNublad


## Installing and testing Cloudy
_from https://gitlab.nublado.org/cloudy/cloudy/-/wikis/DownloadLinks_:
* Download latest Cloudy version ```curl -O https://data.nublado.org/cloudy_releases/c17/c17.02.tar.gz```
* Unzip the file ```tar xvfz /path/to/download-location/c17.02.tar.gz```
* Navigate to folder ```cd c17.02```
* Make the executable ```make```
* Navigate to source ``` cd source ```
* Test installation  ```./cloudy.exe```
* Type "test" then enter twice
* Should print "Cloudy exited OK".

## Running Cloudy

* 
* 


## Input parameters
* Gas density (log scale): 1.7 - 6 (Dense Gas), -3-1.7 (Diffuse Gas)
* Gas phase metallicity: 0.01, 0.05, 0.1, 0.5, 1.0, 2.0 (solar)
* Cosmic ray flux: 1-1e3 x background
* CMD background (z_redshift): 3-15 (or 4-10)
* Raidation spectrum (BPASS): depends on age, metalicity (Z)

## Output params:
* Lines in ```data/LineLabels_filtered.txt```.
