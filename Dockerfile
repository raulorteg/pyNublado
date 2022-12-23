FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y wget && \
    apt install -y git && \
    apt-get -y install python3-pip && \
    wget https://data.nublado.org/cloudy_releases/c17/c17.03.tar.gz --no-check-certificate && \
    tar xvfz c17.03.tar.gz && \
    mv c17.03 ~/c17.03 && \
    cd ~/c17.03/source && \
    make

RUN git clone https://github.com/raulorteg/pyNublado  && \
    mv pyNublado ~/pyNublado && \
    cd ~/pyNublado && \
    python3 -m pip install -r requirements.txt && \
    cd data/BPASS && \
    python3 setup_bpass.py && \
    cd ../../

WORKDIR root/pyNublado/scripts
ENTRYPOINT ["python3"]



