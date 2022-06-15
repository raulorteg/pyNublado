# Installation
pyNublado manages the creation of input scripts for CLOUDY, their execution and parsing of the resulting outputs. The installation has two steps: installing CLOUDY and installing pyNublado

## Requirements
 * Python 3.7 or newer
 * Your favourite C++ compiler to build CLOUDY


## Installing CLOUDY
Instructions from [the Cloudy wiki](https://gitlab.nublado.org/cloudy/cloudy/-/wikis/DownloadLinks):

* Download the latest Cloudy version ```wget https://data.nublado.org/cloudy_releases/c17/c17.02.tar.gz --no-check-certificate```
* Unpack the files ```tar xvfz c17.02.tar.gz```
* Move CLOUDY to the root path ```mv c17.02 ~/c17.02```
* Navigate to the source folder ```cd c17.02/source```
* Build the executable ```make```
Once installed, to test that the installation was successful:
* Run the executable ```~/c17.02/source/cloudy.exe```
* Type "test" then press ```Enter``` twice
* Cloudy should print some output, which ends with "Cloudy exited OK"


## Installing pyNublado

1. Clone the repository ```git clone https://github.com/raulorteg/pyNublado```

##### pip
* Create virtual environment:
    * Update pip ``` python -m pip install pip --upgrade ```
    * Install ``` virtualenv ``` using pip ``` python -m pip install virtualenv ```
    * Create Virtual environment ``` virtualenv pynublado ```
    * Activate Virtual environment (Mac OS/Linux: ``` source pynublado/bin/activate ```, Windows: ``` pynublado\Scripts\activate ```)
    * (_Note: to deactivate environemt run ``` deactivate ```_)
* Install requirements on the Virtual environment ``` python -m pip install -r requirements.txt ```

##### conda
In Anaconda (or Miniconda) environments the requirements can be installed like so:
* ```conda config --add channels conda-forge```
* ```conda install --yes --file requirements_conda.txt```