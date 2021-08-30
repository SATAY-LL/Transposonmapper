

# Statistics per gene 

+++

## The python script
This code determines statistics based on the results obtained in the _pergene.txt file by the Matlab code provided by the Kornmann lab.
The _pergene.txt file consists of three columns.
The rows in the first column contains all genes of * S.Cerevisiae*, the corresponding transposon count is stored in the second column and the third column contains the reads.

The genes in this file are split into two groups based on their essentiality.
This is determined using two files that contains all known essential genes.

The data is represented as a violinplot where both the essential and non-essential genes are shown.

Some basic statistics are determined here, but this can be extended with more if needed.

+++

### Input

Data that needs to be loaded:

1. filepath: Path to the output text file the Matlab code of Benoit that includes the read and transposon count per gene (with extension _pergene.txt)
2. filename: Name of this file.
3. normalize: Whether or not to normalize the transposon and read counts to the gene lengths (True or False)
4. essential_genes_files: List of essential genes. Can be input as multiple files which will be automatically merged.
5. gene_information_file: List of genes with their possible aliasses and lengths in amino acids.


## Interpretation

Initially it is expected that the number of reads and the number of insertions are higher for the non-essential genes as these are more tolerant to transposons than the essential genes.
Note that 'essential' means 'annotated essential' here, and not 'essential based on the data'.
It might occur that genes are annotated as (non-)essential, but that this does not agree with the data.
This might skew the data shown in the graphs, but since it is expected that these situations do not occur frequently these graphs can still give a good indication about the differences in number of reads and insertions per (non-)essential gene.

Ideally the median values of the essential and nonessential genes are far apart from each other, so that a clear distinction can be made between which genes are essential and which are not based on the transposon counts. If this is not the case or when there is significant overlap between the distribution, no definite conclusion can be drawn about the essentiality.

Usually, essential genes have little transposon counts, but nonessential genes can have both high or low transposon counts (for an explanation on this effect, see the paper by Michel et.al. 2017).
This means that if a high transposon count occurs, the gene is probably nonessential.
But if a low transposon count is present, typically no definite conclusion can be drawn about its essentiality.

+++

## Bibliography
- Michel, A. H., Hatakeyama, R., Kimmig, P., Arter, M., Peter, M., Matos, J., ... & Kornmann, B. (2017). Functional mapping of yeast genomes by saturated transposition. Elife, 6, e23570.
- Segal, E. S., Gritsenko, V., Levitan, A., Yadav, B., Dror, N., Steenwyk, J. L., ... & Kunze, R. (2018). Gene essentiality analyzed by in vivo transposon mutagenesis and machine learning in a stable haploid isolate of Candida albicans. MBio, 9(5), e02048-18.
