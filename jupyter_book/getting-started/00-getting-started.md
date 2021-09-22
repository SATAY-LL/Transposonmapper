# Installing transposonmapper

```{note}
Installing the transposonmapper package is optional. When running SATAY from the docker container, transposonmapper is pre-installed. 
```

## Installing Transposonmapper from PyPi 

For users that only require post processing analysis of the data (the bam file was already analyzed),
do use the default installation. For example `pysam` won't be installed, hence Linux is not required.


```bash

   pip install transposonmapper 

```

For users that require the whole processing pipeline, do use: 


```bash

   pip install transposonmapper[linux]
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