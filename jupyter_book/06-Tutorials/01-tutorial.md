
# Tutorial-1 : How to run the transposonmapper python package in a specific environment.  



### Installing python package for users 

```bash 

git clone https://github.com/SATAY-LL/Transposonmapper.git Transposonmapper
cd Transposonmapper
conda env create --file conda/environment.yml
conda activate satay
pip install -e .

```


### Installing python package for developers

```bash 

git clone https://github.com/SATAY-LL/Transposonmapper.git Transposonmapper
cd Transposonmapper
conda env create --file conda/environment-dev.yml
conda activate satay-dev
pip install -e .[dev]

```

### Importing the required python libraries 


```python
import os, sys
import warnings
import timeit
import numpy as np
import pysam
import pandas as pd 

# importing the transposon mapping function

from transposonmapper  import transposonmapper


```



## Invoking the transposonmapper package with a dummy file


```python
bamfile= '../transposonmapper/data_files/files4test/SRR062634.filt_trimmed.sorted.bam'
filename='SRR062634.filt_trimmed.sorted.bam'
assert os.path.isfile(bamfile), "Not a file or directoy"

transposonmapper(bamfile=bamfile) 
```


