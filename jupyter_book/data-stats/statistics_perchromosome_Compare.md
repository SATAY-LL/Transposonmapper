

# Comparison of the statistics per chromosome

+++

## Introduction

This script gives a numerical overview of the two datasets in the form of a textfile.
This can be used for comparing statistical values of two datasets.

+++

## The python script
The script inputs two .bed files in a list that were generated using the Matlab code provided by the Kornmann lab and the path and name of a text file where the results will be written.
Currently 11 different statistical values are determined, but this can be easily extended (see explainatory text between the codes below).

1. Number of transposon insertions.
2. Percentage of the chromosome that is covered by transposons
3. Mean distance between transposon insertions.
4. Median distance between transposon insertions.
5. 25th percentile of the distance between transposon insertions.
6. 75th percentile of the distance between transposon insertions.
7. Largest area devoid of transposons
8. Mean number of reads per transposon
9. Median numbr of reads per transposon
10. 25th percentile reads per transposon
11. 75th percentile reads per transposon


+++

### Input
The function inputs either a gene name (`gene_name`, type=string) or a region (`region`, type=list) specified as a list with three entries (chromosome number as a roman numeral, start position of the region and the end position respectively).
The variable `gene_name` can be set to any gene name or `holocus` or `ho-locus`.
Next it requires the bed-file (`bed_file`, type=string) which is created by the Matlab code provided from [the Kornman lab](https://sites.google.com/site/satayusers/complete-protocol/bioinformatics-analysis/matlab-script).
Finally, the figure can be automatically saved (at a location specified in the beginning of the function) by setting `savefigure` to `True`.

The custom build functions (stored in the ['python modules' folder on Github](https://github.com/Gregory94/LaanLab-SATAY-DataAnalysis/tree/master/python_modules)) that are required are:
- chromosome_and_gene_positions.chromosome_position
- chromosome_and_gene_positions.chromosome_roman_to_arabic
- chromosome_names_in_fies.chromosome_name_bedfile


### Get chromosome information

Determine the lengths and position of the different chromosomes and get a list of the chromosome names in terms of roman numerals.



### Create lists for the variables

All the variables that are determined are put in individual lists.
When new statistics needs to be determined, add a new list for each new value.


### Determine statistics

For each chromosome in each .bed file the statistical values are determined and stored in the respective lists.
The values are also determined for the entire genome.

First a for loop is done over all bed files and for each bed file the names of the chromosomes as they are stored in the bed files are determined.
Next, some statistical values are determined and depending whether it is first file written a text file is generated or the values are appended to the already exsiting text file.
After all chromosomes the statistics are determined for the entire genome as well.



### Creating text file

Write the stored statistical value to the text file.


### Printing result

Showing part of the text file to give an example of the created text file.
(This is just for showing the result in this notebook and is not important for the code itself.
Can be removed).



## Interpretation

The statistical values that are determined here for two datasets give an indication of some of the properties of the datasets.
Together with the TransposonRead_Profile_Compare.py script, this can be helpful when comparing two datasets with each other to possibly improve the preprocessing steps.
This script can relatively easy be extended with more statistical values in the future.

The `Coverage percentage` is the number of transposons divided by the number of basepairs of the chromosome.
The distance between transposon insertions is determined by the taking the absolute difference between all subsequent transposon and for the first and last transposon the distance is determined from the beginning and until the end of the chromosome, respectively.
The same goes for the median and the percentiles.
The largest distance between subsequent transposons is displayed as the largest area devoid of transposons.
The values regarding the number of reads are directly extracted from the bed files.

+++

## Bibliography
- Michel, A. H., Hatakeyama, R., Kimmig, P., Arter, M., Peter, M., Matos, J., ... & Kornmann, B. (2017). Functional mapping of yeast genomes by saturated transposition. Elife, 6, e23570.
