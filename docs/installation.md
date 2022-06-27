# Installation
pyNublado manages the creation of input scripts for Cloudy runs, their execution, and parsing of the resulting outputs. This installation guide has two steps: installing CLOUDY and installing pyNublado

### Requirements
 * Python 3.7 or newer
 * Your favourite C++ compiler to build Cloudy


### Installing CLOUDY
Instructions from [the Cloudy wiki](https://gitlab.nublado.org/cloudy/cloudy/-/wikis/DownloadLinks):

* Download the latest Cloudy version

  ```bash
  wget https://data.nublado.org/cloudy_releases/c17/c17.03.tar.gz --no-check-certificate
  ```
* Unpack the files

  ```bash
  tar xvfz c17.03.tar.gz
  ```
* Move the extracted Cloudy folder to where you want it to live, e.g. your home directory

  ```bash
  mv c17.03 ~/c17.03
  ```
* Navigate to the source folder 

  ```bash 
  cd ~/c17.03/source
  ```
* Build the executable 

  ```bash
  make
  ```
  
Once installed, you can test whether the installation was successful:
* Run the executable

  ```bash 
  ~/c17.03/source/cloudy.exe
  ```

* Type "test" then press ```Enter``` **twice**
* Cloudy should print some output, which ends with "Cloudy exited OK"


### Installing pyNublado

1. Clone the repository

   ```bash 
   git clone https://github.com/raulorteg/pyNublado
   ```

2. Install all dependencies, either via **pip** or **conda**

#### pip
* Create virtual environment:
    * Update pip ``` python -m pip install pip --upgrade ```
    * Install ``` virtualenv ``` using pip ``` python -m pip install virtualenv ```
    * Create Virtual environment ``` virtualenv pynublado ```
    * Activate Virtual environment (Mac OS/Linux: ``` source pynublado/bin/activate ```, Windows: ``` pynublado\Scripts\activate ```)
    * Note: to deactivate environmet run ``` deactivate ```
* Install requirements on the Virtual environment ``` python -m pip install -r requirements.txt ```

#### conda
In an existing Anaconda (or Miniconda) environment the requirements can be installed like so:

* ```bash
  conda config --add channels conda-forge
  ```

* ```bash
  conda install --yes --file requirements_conda.txt
  ```