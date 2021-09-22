

## Tutorial-2 :  How to clean the wig and bed files. 

After following the steps in  {doc}`01-tutorial`

Here we will remove transposon insertions in .bed and .wig files that were mapped outside the chromosomes, creates consistent naming for chromosomes and change the header of files with custom headers.

## Import the function

```python
from transposonmapper.processing.clean_bedwigfiles import cleanfiles
```
### Lets save the wig and bed files as variables to clean them and call the function.

Lets use our dummy files that were outputed after running transposonmapper in {doc}`01-tutorial`

```python

wig_files=[]
bed_files=[]

#data_dir= "../satay/data_files/data_unmerged/"
data_dir="../transposonmapper/data_files/files4test/"
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith("sorted.bam.wig"):
            wig_files.append(os.path.join(root, file))
        elif file.endswith("sorted.bam.bed"):
             bed_files.append(os.path.join(root, file))
```
##  Cleaning the files 

### What for?
Clean wig files for proper visualization in the genome Browser http://genome-euro.ucsc.edu/cgi-bin/hgGateway

``` python

custom_header = ""
split_chromosomes = False
for files in zip(wig_files,bed_files):
    cleanfiles(filepath=files[0], custom_header=custom_header, split_chromosomes=split_chromosomes)
    cleanfiles(filepath=files[1], custom_header=custom_header, split_chromosomes=split_chromosomes)

```


