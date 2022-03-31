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
wget https://data.nublado.org/cloudy_releases/c17/c17.02.tar.gz --no-check-certificate
```
* Unpack the files
```bash
tar xvfz c17.02.tar.gz
```
* Navigate to the source folder
```bash
cd c17.02/source
```
* Build the executable
```bash
make
```
* Test the installation  
```bash
./cloudy.exe
```
* Type "test" then Enter twice
* Cloudy should print some output, which ends with "Cloudy exited OK"

* Set PATH variables? tba

### Python modules
tba


## Running Cloudy

*
*


## Input parameters
* Gas density (log scale): -3-6
* Gas phase metallicity: 0.01 - 2.0 (solar)
* CMD background (z_redshift): 3-12
* Radiation spectrum (BPASS), Chabrier IMF, Mup=300 Msun: depends on age, metalicity (Z)
* ages (is delimited by the redshift): 1 Myr up to 2 Gyr.
* Metalicity (Z): 1e-5-0.040 (absolute value)


## Output params:
* Lines in ```data/LineLabels_filtered.txt```.
