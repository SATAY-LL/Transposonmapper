 ## Python scripts

The software discussed in the previous section is solely for the processing of the data.
The codes that are discussed here are for the postprocessing analysis.
These are all python scripts that are not depended on Linux (they run and are tested in Windows) and only use rather standard python package like numpy, matplotlib, pandas, seaborn and scipy.
The python version used for creating and testing is Python v3.8.5.

The order in which to run the programs shouldn't matter as these scripts are all independed of each other except for genomicfeatures_dataframe.py which is sometimes called by other scripts.
However, most scripts are depending on one or more python modules, which are all expected to be located in a python_modules folder inside the folder where the python scripts are located (see [github](https://github.com/Gregory94/LaanLab-SATAY-DataAnalysis/tree/satay_processing/python_scripts) for an example how this is organized).
Also many python scripts and modules are depending on data files stored in a folder called data_files located in the same folder of the python_scripts folder.
The input for most scripts and modules are the output files of the processing.

This is a typical order which can be used of the scripts described below:

1. clean_bedwigfiles.py (to clean the bed and wig files).
2. transposonread_profileplot_genome.py (to check the insertion and read distribution throughout the genome).
3. transposonread_profileplot.py (to check the insertions and read distribution per chromosome in more detail).
4. scatterplot_genes.py (to check the distribution for the number of insertions per gene and per essential gene).
5. volcanoplot.py (only when comparing multiple datasets with different genetic backgrounds to see which genes have a significant change in insertion and read counts).

Most of the python scripts consists of one or more functions.
These functions are called at the end of each script after the line `if __name__ == '__main__':`.
The user input for these functions are stated at the beginning of the script in the `#INPUT` section.
All packages where the scripts are depending on are called at the beginning of the script.
The scripts also contain a help text about how to use the functions.
