# pyNublado

A package to run Cloudy models.

## Setup
### Requirements
 * Python 3.7 or newer
 * Your favourite C++ compiler to build Cloudy


### Installing and testing Cloudy
Instructions from https://gitlab.nublado.org/cloudy/cloudy/-/wikis/DownloadLinks:
* Download the latest Cloudy version
```bash 
curl -O https://data.nublado.org/cloudy_releases/c17/c17.02.tar.gz
```
* Unzip the file
```bash
tar xvfz /path/to/download-location/c17.02.tar.gz
```
* Navigate to folder
```bash
cd c17.02/source
```
* Make the executable
```bash
make
```
* Test installation  
```bash
./cloudy.exe
```
* Type "test" then enter twice
* Cloudy should print "Cloudy exited OK".

* Set PATH variables? tba

### Python modules
tba


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
