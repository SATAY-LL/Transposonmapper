
# Gene reads script

+++

## Introduction
To get an indication of possible essential genes, the number of transposon insertions and amount of reads per transposon is plotted along the length of the gene. If a gene consists of a large area without any insertions or with little reads, this might indicate an essential (region of a) gene.
However, it sometimes might happen that non-essential genes have no transposons. This can mulitple reasons, most notable which are:
- Sequencing reads that map to repeated sequences were discarded during alignment. If these repeated sequences occur in protein coding regions in the genome, then these regions might be removed during alignment and therefore these genes appear to be free of transposon, even though these genes might not be essential.
- Annotated dubious ORFs might overlap with essential genes. So the dubious ORFs are not essential, but have no insertions because of the overlap.
- Sometimes genes might not be essential in normal growth conditions (and hence are not annotated as such), but in particular lab conditions some genes can become essential (for example genes involved in the metabolism of certain sugars).

Also, sometimes transposons occur in essential genes. This can be because not the complete gene is essential, but only certain domains of the gene are essential. The non-essential domain can be truncated and still create a function protein with only the essential domains left. Also, sometimes the first and/or last few basepairs can be truncated while still leave a gene that can be transcribed and translated in a functional protein.

For a more thorough discussion, see the paper from Michel et.al. 2017.

+++

## The python script
This function creates a bar plot with the number of reads per transposon for regions in a gene. It also shows the exact locations of the insertions along the gene. The width of the bars are chosen such that each bar include a fixed amount of transposons. A maximum threshold is set to account for the situation where there are little or no transposons present for large portion of the gene.

Next to the bar plot, this function also creates a violin plot where a distribution is shown for the distance (in terms of basepairs) between subsequent insertions. This is compared with the distance between insertions in the entire chromosome the gene is in. If the median distance between insertions is significantly higher in the gene compared to the chromosome, then this might be an indication of an essential gene.

+++

### Input
The function inputs either a gene name (`gene_name`, type=string) or a region (`region`, type=list) specified as a list with three entries (chromosome number as a roman numeral, start position of the region and the end position respectively).
The variable `gene_name` can be set to any gene name or `holocus` or `ho-locus`.
Next it requires the bed-file (`bed_file`, type=string) which is created by the Matlab code provided from the Kornman lab [https://sites.google.com/site/satayusers/complete-protocol/bioinformatics-analysis/matlab-script].
Finally, the figure can be automatically saved (at a location specified in the beginning of the function) by setting `savefigure` to `True`.

The custom build functions (stored in the 'python modules' folder on Github [https://github.com/Gregory94/LaanLab-SATAY-DataAnalysis/tree/master/python_modules]) that are required are:
- chromosome_and_gene_positions.gene_position
- gene_names.gene_aliases
- chromosome_names_in_files.chromosome_props_bedfile
- statistics_perchromosome



### Get start and end position of the gene or region
When a gene name is given, this part searches in the .gff file for the position and reading orientation of the gene.
However, often genes have multiple names and the name given by the user might be present as such in the .gff file.
Therefore this code searches for potential aliases of the gene name in the Yeast_Protein_Names.txt file.



### Get the reads
Next, get the reads per transposon as stored in the bed file. For this the bed file is read and the lines are determined where in the bed file the insertions are for the chromosome where the gene is located in (using the chromosome_props_bedfile.py module). Within the chromosome, the insertion locations are searched that fall within the location of the gene.
the values for the reads that found in the bed file are determined by taking the value -100 and divided by 20. This is undo what is done in the Matlab code by Benoit for better visualization, but in this code we want to take the actual values and therefore the formula used by the Matlab code is reversed.


### Consider double insertions
Sometimes a single location has multiple insertions. This piece of code makes sure that the reads from all insertions at the same loation are accounted for.



### Create list of all locations in the gene
Create a list with the same length as the number of basepairs in the gene where for each location the number of reads are stored.



### Statistics and prepare for plotting
Some statistical values are determined, like the average number insertions as well as the median, the percentiles and the coverage. Also the number of basepairs between the insertions are determined here.


### Binning
The gene is divided in several bins. The width of the bins are determined to include 8 transposons. So if there are many transposons close together, the bin width will be small whereas insertions that are well separated results in large bins.
To account for the situation that are very little insertions or no insertions at all, a maximum bin width is determined to be 8 times the average distance between insertions for the entire chromosome.


### Plotting
Make the bar plot and the violinplot.



## Interpretation
The resulting barplot shows the insertions (represented by the small black bars) along the gene. The blue bars indicate the number of reads per transposon in that bin. This shows how the insertions and reads are distributed along the gene.
The reading orientation is indicated by a + (forward reading) or - (reverse reading). The numbers for the mean are given together with the standard deviation (note that this is typically very large). Therefore a more reliable measure might be the percentiles given as the 25th, 50th and the 75th percentile respectively.

The violinplot shows the distribution of the amount of basepairs between subsequent insertions for both the gene (green) and the chromomsome the gene is in (red). A significant difference in the median basepairs between insertions might indicate potential essential genes.

+++

## Bibliography
- Michel, A. H., Hatakeyama, R., Kimmig, P., Arter, M., Peter, M., Matos, J., ... & Kornmann, B. (2017). Functional mapping of yeast genomes by saturated transposition. Elife, 6, e23570.
