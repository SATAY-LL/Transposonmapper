
## Python Translation of the Matlab code from Kornmann Lab  

This is a tool developed for analysing transposon insertions for experiments using SAturated Transposon Analysis in Yeast (SATAY).
This python code contains one function called transposonmapper().
For more information about this code and the project, see [HERE](github.com/Gregory94/LaanLab-SATAY-DataAnalysis)

This code is based on the Matlab code created by the Kornmann lab which is available at [HERE](sites.google.com/site/satayusers/) 

``` bash
__Author__ = Gregory van Beek. LaanLab, department of Bionanoscience, Delft University of Technology
__version__ = 1.4
__Date last update__ = 2020-08-09
``` 


```{admonition} Version history:
- 1.1; Added code for creating two text files for storing insertion locations per gene and per essential gene [2020-07-27]
- 1.2; Improved searching algorithm for essential genes [2020-08-06]
- 1.3; Load file containing all essential genes so that a search for essential genes in multiple file is not needed anymore. This file is created using Create_EssentialGenes_list.py located in the same directory as this code [2020-08-07]
- 1.4; Fixed bug where the gene position and transposon insertion location did not start at zero for each chromosome, causing confusing values to be stored in the _pergene_insertions.txt and _peressential_insertions.txt files [2020-08-09]
``` 


**This function is created for analysis of SATAY data using the species Saccharomyces Cerevisiae.**

#### Outputs: 
- It outputs the following files that store information regarding the location of all insertions:

    - .bed-file: Includes all individual basepair locations of the whole genome where at least one transposon has been mapped and the number of insertions for each locations (the number of reads) according to the Browser Extensible Data (bed) format.

        - A distinction is made between reads that had a different reading orientation during sequencing. The number of reads are stored using the equation #reads*20+100 (e.g. 2 reads is stored as 140).

    - .wig-file: Includes all individual basepair locations of the whole genome where at least one transposon has been mapped and the number of insertions for each locations (the number of reads) according to the Wiggle (wig) format.

            - In this file no distinction is made between reads that had a different reading orientation during sequencing. The number of reads are stored as the absolute count.

    - _pergene.txt-file: Includes all genes (currently 6600) with the total number of insertions and number of reads within the genomic region of the gene.

    - _peressential.txt-file: Includes all annotated essential genes (currently 1186) with the total number of insertions and number of reads within the genomic region of the gene.

    - _pergene_insertions.txt-file: Includes all genes with their genomic location (i.e. chromosome number, start and end position) and the locations of all insertions within the gene location. It also include the number number of reads per insertions.

    - _peressential_insertions.txt-file: Includes all essential genes with their genomic location (i.e. chromosome number, start and end position) and the locations of all insertions within the gene location. It also include the number number of reads per insertions.

    - (note that in the latter two files, the genomic locations are continous, for example chromosome II does not start at 0, but at 'length chromosome I + 1' etc.).
- The output files are saved at the location of the input file using the same name as the input file, but with the corresponding extension.

- **The function assumes that the reads are already aligned to a reference genome.**

#### Inputs 
- The input data should be a .bam-file and the location where the .bam-file is stored should also contain an index file (.bam.bai-file, which for example can be created using sambamba).
  
This function takes the following inputs:

- bamfile [required]: Path to the bamfile. This location should also contain the .bam.bai index file (does not need to be input in this function).

- gfffile [optional]: Path to a .gff-file including all gene information (e.g. downloaded from SGD). Default file is 'Saccharomyces_cerevisiae.R64-1-1.99.gff3'.

- essentialfiles [optional]: Path to a .txt file containing a list all essential genes. Every line should consist of a single essential gene and the file should have one header line. Ideally this file is created using 'Create_EssentialGenes_list.py'. 
Default file is 'Cerevisiae_AllEssentialGenes_List.txt'.

- genenamesfile [optional]: Path to text file that includes aliases for all genes. Default file is 'Yeast_Protein_Names.txt'.

When the arguments for the optional files are not given, the files are used that are stored at the following location: ```path_current_pythonscript/../data_files```
    
The function uses the pysam package for handling bam files (see pysam.readthedocs.io/en/latest/index.html) and therefore this function only runs on Linux systems with SAMTools installed.


