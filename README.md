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

### Using BPASS models
* From the BPASS V2.2.1 [data release](https://bpass.auckland.ac.nz/9.html) download the data for _bpass_v2p2.1_imf_chab300_


_NOTE: the Perl script (in data/) needs to be placed on the parent directory_

```bash
├── BPASSv2.1_bin-imf135_300
│   ├── ...
│   └── ...
├── convert_bpassv2.x.pl
```

* Navigate to the BPASS folder ```cd BPASSv2.1_bin-imf135_300 ```
* Execute the Perl script from the folder
``` ../convert_bpassv2.x.pl```

_NOTE: If it complains about permissions grant the Perl file permissions_

```bash
chmod +x convert_bpassv2.x.pl
```
* Generate binary files from the resulting _.ascii_ files excuting CLOUDY ```~/c17.02/source/cloudy.exe```
* Press ```enter```
* Type ```compile star BPASSv2_imf135_100_burst_binary.ascii" ```
* Press ```enter``` again to generate the binaries.

The binaries now need to be placed in a special location for CLOUDY to use them.

* Navigate to the CLOUDY data directory ```cd ~/c17.02/data```
* Create a binaries directory ```mkdir binaries```
* Finally copy the binary BPASS file to the binaries/ directory ``` cp bpass_v2p2.1_imf_chab300_burst_binary.mod ~/c17.02/data/binaries/```

## Running Cloudy

Example of running CLOUDY indendently:
1. Create a _[name].in_ file
2. Navigate to the folder where the .in file is
3. Execute CLOUDY from the directory ```~/c17.02/source/cloudy.exe [name].in```


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
