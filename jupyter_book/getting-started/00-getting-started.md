# Installing transposonmapper

```{note}
Installing the transposonmapper package is optional. When running SATAY from the docker container, transposonmapper is pre-installed. Also, the transposonmapper package requires the `pysam` package, which only runs on a Linux system.
```

## Installing Transposonmapper from PyPi (work in progress)
In a terminal, enter

```bash

pip install transposonmapper 

```

## Installing Transposonmapper from the GitHub repository 
We recommend using conda as a virtual environment manager to isolate installed dependencies. 

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