
# What is SATAY

SAturated Transposon Analysis in Yeast (SATAY) is method of transposon analysis optimised for usage in Saccharomyces Cerevisiae.

This method uses transposons (short DNA sequences, also known as jumping genes) which can integrate in the native yeast DNA at random locations.

A transposon insertion in a gene inhibits this gene to be translated into a functional protein, thereby inhibiting this gene function.

The advantage of this method is that it can be applied in many cells at the same time.
Because of the random nature of the transposons the insertion coverage will be more or less equal over the genome.

When enough cells are used it is expected that, considering the entire pool of cells, all genes will be inhibited by at least a few transposons.

### What are transposons? 

- Transposons are small pieces of DNA that can integrate in a random location in the genome.
When the insertion happens at the location of a gene, this gene will be inhibited (i.e. it can still be transcribed, but typically it cannot be translated into a functional protein).

- After a transposon is randomly inserted in the DNA, the growth of the cell is checked.
- If the cell cannot produce offspring, the transposon has likely been inserted in an essential gene or genomic region.
- This is done for many cells at the same time.



### What happens after the cells have had  one transposon insertion? 

After a transposon insertion, the cells are given the opportunity to grow and proliferate.

Cells that have a transposon inserted in an essential genomic region (and thus blocking this essential function), will proliferate only very little or not at all (i.e. these cells have a low fitness) whilst cells that have an insertion in a non-essential genomic region will generate significantly more daughter cells (i.e. these cells have a relative high fitness).
The inserted transposon DNA is then sequenced together with a part of the native yeast DNA right next to the transposon.

This allows for finding the genomic locations where the transposon is inserted by mapping the sequenced native DNA to a reference genome.

Non-essential genomic regions are expected to be sequenced more often compared to the essential regions as the cells with a non-essential insertion will have proliferated more.

Therefore, counting how often certain insertion sites are sequenced is a method for probing the fitness of the cells and therefore the essentiality of genomic regions.
For more details about the experimental approach, see the paper from Michel et.al. 2017 and this website from [the Kornmann-lab](https://sites.google.com/site/satayusers/).



This method needs to be performed on many cells to ensure a high enough insertion coverage such that each gene is inhibited in at least a few different cells.
After transposon insertion and proliferation, the DNA from each of these cells is extracted and this is sequenced to be able to count how often each genomic region occurs.
This can yield tens of millions of sequencing reads per dataset that all need to be aligned to a reference genome.
In order to that we have **Transposonmapper**
which is  a processing workflow  that takes  the raw sequencing data and outputs lists of all insertion locations together with the corresponding number of reads.

This workflow consists of quality checking, sequence trimming, alignment, indexing and transposon mapping.
This documentation explains how each of these steps are performed, how to use the workflow and discusses some python scripts for checking the data and for postprocessing analysis.


`
