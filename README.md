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
The following Python modules are needed

* numpy
* matplotlib
* astropy
* pyDOE
* ...

##### pip
The Python dependencies can be installed with `pip` like so:
```bash
pip3 install -r requirements.txt
```

##### conda
In Anaconda (or Miniconda) environments the requirements can be installed like so:
```bash
conda config --add channels conda-forge
conda install --yes --file requirements_conda.txt
```

### Preparing the BPASS models
* From the BPASS V2.1 [data release](https://bpass.auckland.ac.nz/8.html) download the data for [BPASSV2.1_bin-imf135_300](https://drive.google.com/drive/folders/0B7vqPPPgOdtIaUdWRElMMDdHSG8?resourcekey=0-pIKN3NE1KTpfbEfr_K_Rcw)
* Use the [pearl script](https://data.nublado.org/stars/convert_bpassv2.x.pl) to convert the data to ascii format readable for CLOUDY:

_NOTE: the pearl script needs to be placed on the parent directory_

```bash
├── BPASSv2.1_bin-imf135_300
│   ├── ...
│   └── ...
├── convert_bpassv2.x.pl
```

* Navigate inside the BPASS folder
```bash
cd BPASSv2.1_bin-imf135_300
```
* Execute the pearl script from the folder
```bash
../convert_bpassv2.x.pl
```
_NOTE: If it complains about permissions grant the pearl file permissions_
```bash
chmod +x convert_bpassv2.x.pl
```
* Generate binary files from the resulting _.ascii_ files using CLOUDY
```
cloudy
```
* Type enter, then ```compile star "BPASSv2_imf135_100_burst_binary.ascii" ``` then enter again.


## Running Cloudy

*
*


## Input parameters
* Gas density (log scale): -3 - 6
* Gas phase metallicity: 0.0001 - 2.0 (solar) #NOTE: sampled in log space
* CMB background (z_redshift): 3-12
* Ionization parameter: -4 - 0 (log units)
* Radiation spectrum (BPASS), Chabrier IMF, Mup=300 Msun: depends on age, metalicity (Z)
    * Stellar ages (is delimited by the redshift): 1 Myr up to 2 Gyr.
    * Stellar Metalicity (Z): 1e-5-0.040 (absolute value)


## Output params:
* Lines in ```data/LineLabels_filtered.txt```.
