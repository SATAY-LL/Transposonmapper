
# Installation

## Installing Transposonmapper from PyPi (work on progress)

```bash

pip install transposonmapper

```

## Installing Transposonmapper from the github repository 

### For users 

```bash 

git clone https://github.com/SATAY-LL/Transposonmapper.git Transposonmapper
cd Transposonmapper
conda env create --file conda/environment.yml
conda activate satay
pip install -e .

```

### For developers

```bash 

git clone https://github.com/SATAY-LL/Transposonmapper.git Transposonmapper
cd Transposonmapper
conda env create --file conda/environment-dev.yml
conda activate satay-dev
pip install -e .[dev]

```