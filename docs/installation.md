# Installation
pyNublado manages the creation of input scripts for Cloudy runs, their execution, and parsing of the resulting outputs. This installation guide gives two options to install and use CLOUDY & pyNublado: Installing them directly or using Docker. 


## Using Docker
For information about Docker a good reference is their documentation [https://www.docker.com/](https://www.docker.com/).

1. First build the image using the ```Dockerfile``` provided:
  ```bash
  sudo docker build . --tag="pynublado:latest"
  ```

2. Once built we can then run our application on the Docker container. 
  ```bash
  sudo docker run -v $PWD/data:/root/pyNublado/data -it --rm  "pynublado:latest" hpc.py --N_sample=<N_sample> --N_cpus=<N_cpus>
  ```


## Installing CLOUDY & pyNublado

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