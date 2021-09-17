# Detailed description of the output files from satay.sh


## Recap on how the sequencing works 

- To get the order of nucleotides in a genome, shotgun sequencing is used where the genome is cut is small pieces called reads (typically tens to a few hundred basepairs long).
- The reads have overlapping regions that can be used to identify their location with respect to a reference genome and other reads (i.e. mapping of the reads).
- Mapping of the reads result in contigs, which are multiple mapped reads that form continuous assembled parts of the genome (contigs can be the entire target genome itself).
- All contigs should be assembled to form (a large part of) the target genome.

- The sequence assembly problem can be described as: *Given a set of sequences, find the minimal length string containing all members of the set as substrings*.

The reads from the sequencing can be single-end or paired-end, which indicates how the sequencing is performed.

In paired-end sequencing, the reads are sequenced from both directions, making the assembly easier and more reliable, but results in twice as many reads as single-end reads.

The reason of the more reliable results has to do with ambiguous reads that might occur in the single-end sequencing.
Here, a read can be assigned to two different locations on the reference genome (and have the same alignment score).
In these cases, it cannot be determined where the read should actually be aligned (hence its position is ambiguous).

In paired-end sequencing, each DNA fragment has primers on both ends, meaning that the sequencing can start in both the 5’-3’ direction and in the 3’-5’ direction.
Each DNA fragment therefore has two reads both which have a specified length that is shorter than the entire DNA fragment.

This results that a DNA fragment is read on both ends, but the central part will still be unknown (as it is not covered by these two particular reads, but it will be covered by other reads).
Since you know that the two reads belong close together, the alignment of one read can be checked by the alignment of the second read (or paired mate) somewhere in close vicinity on the reference sequence.
This is usually enough for the reads to become unambiguous.


## Sequencing data processing : satay.sh 

The resulting data from the sequencing is stored in a FASTQ file where all individual reads are stored including a quality score of the sequencing.
The reads are in random order and therefore the first step in the processing is aligning of the reads in the FASTQ files with a reference genome.

Note that the quality of the reads typically decreases near the 3'-end of the reads due to the chemistry processes required for sequencing (this depends on the kind of method used).
For Illumina sequencing, the main reasons are signal decay and dephasing, both causing a relative increase in the background noise.
Dephasing occurs when a DNA fragment is not de-blocked properly.
A DNA fragment is copied many times and all copies incorporate a fluorescent nucleotide that can be imaged to identify the nucleotide.
If there are 1000 copies of the DNA fragment, there are 1000 fluorescent nucleotides that, ideally, are all the same to create a high quality signal.
After imaging, the DNA fragment is de-blocked to allow a new fluorescent nucleotide to bind.
This deblocking might not work for all copies of the DNA fragment.

For example, 100 copies might not be deblocked properly, so for the next nucleotide only 900 copies agree for the next incorporated nucleotide.
For the third round, the 100 copies that were not deblocked properly in the second round, might now be deblocked as well, but now they are lagging behind one nucleotide, meaning that in the coming rounds they have consistently the wrong nucleotide.

As the reads increases in length, more rounds are needed and therefore the chances of dephasing increases causing a decrease in the quality of the reads.
This gives noise in the signal of the new nucleotide and therefore the quality of the signal decreases.
For example, take the next 6bp sequence that is copied 5 times:

1. `GATGTC`
2. `GATGTC`
3. `G ATGT`
4. `GAT GT`
5. `G AT G`

The first two reads are deblocked properly and they give all the right nucleotides.
But the third and fourth have one round that is not deblocked properly (indicated by the empty region between the nucleotides), hence the nucleotide is always lagging one bp after the failed deblocking.
The fifth copy has two failed deblocking situations, hence is lagging two bp.

The first nucleotide is a G for all 5 copies, therefore the quality of this nucleotide is perfect.
But, by the end of the read, only two out of five copies have the correct bp (i.e. a C), therefore the quality is poor for this nucleotide.
(It can either be a C or a T with equal likelyhood or potentially a G, so determining which nucleotide is correct is ambiguous without knowing which reads are lagging, which you don't know).

(See for example [this question on seqanswers](http://seqanswers.com/forums/showthread.php?t=61198) or the paper by [Pfeifer, 2016])

## File Types 

### fastq

This is the standard output format for sequencing data.
It contains all (raw) sequencing reads in random order including a quality string per basepair.
Each read has four lines:

1. Header: Contains some basic information from the sequencing machine and a unique identifier number.
2. Sequence: The actual nucleotide sequence.
3. Dummy: Typically a '+' and is there to separate the sequence line from the quality line.
4. Quality score: Indicates the quality of each basepair in the sequence line (each symbol in this line belongs to the nucleotide at the same position in the sequence line). The sequence and this quality line should always have the same length.

The quality line is given as a phred score.
There are two versions, base33 and base64, but the base64 is outdated and hardly used anymore.
In both versions the quality score is determined by Q = -10*log10(P) where P is the error probability determined during sequencing (0 < P < 1).
A Q-score of 0 (i.e. an error probability of P=1) is defined by ascii symbol 33 ('!') for base33 and by ascii symbol 64 ('@') for base64.
A Q-score of 1 (p=0.79) is then given by ascii 34 (' " ') (for base33) etcetera.
For a full table of ascii symbols and probability scores, see the appendices of this document [PHRED table (base33)](#phred-table-base33) and [PHRED table (base64)](#phred-table-base64).
Basically all fastq files that are being created on modern sequencing machines use the base33 system.

The nucleotide sequence typically only contains the four nucleotide letters (A, T, C and G), but when a nucleotide was not accurately determined (i.e. having a error probability higher than a certain threshold), the nucleotide is sometimes converted to the letter N, indicating that this nucleotide was not successfully sequenced.

Fastq files tend to be large in size (depending on how many reads are sequenced, but >10Gb is normal).
Therefore these files are typically compressed in gzip format (.fastq.gz).
The pipeline can handle gzipped files by itself, so there is no need to convert it manually.

Example fastq file:

> `@NB501605:544:HLHLMBGXF:1:11101:9938:1050 1:N:0:TGCAGCTA`  
> `TGTCAACGGTTTAGTGTTTTCTTACCCAATTGTAGAGACTATCCACAAGGACAATATTTGTGACTTATGTTATGCG`  
> `+`  
> `AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE`  
> `@NB501605:544:HLHLMBGXF:1:11101:2258:1051 1:N:0:TACAGCTA`  
> `TGAGGCACCTATCTCAGCGATCGTATCGGTTTTCGATTACCGTATTTATCCCGTTCGTTTTCGTTGCCGCTATTT`  
> `+`  
> `AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE6EEEEEEEE<EEEAEEEEEEE/E/E/EA///`  
> `@NB501605:544:HLHLMBGXF:1:11101:26723:1052 1:N:0:TGCAGCTA`  
> `TGTCAACGGTTTAGTGTTTTCTTACCCAATTGTAGAGACTATCCACAAGGACAATATTTGTGACTTATGTTATGCG`  
> `+`  
> `AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE`

### sam, bam

When the reads are aligned to a reference genome, the resulting file is a Sequence Alignment Mapping (sam) file.
Every read is one line in the file and consists of at least 11 tab delimited fields that are always in the same order:

1. Name of the read. This is unique for each read, but can occur multiple times in the file when a read is split up over multiple alignments at different locations.
2. Flag. Indicating properties of the read about how it was mapped (see below for more information).
3. Chromosome name to which the read was mapped.
4. Leftmost position in the chromosome to which the read was mapped.
5. Mapping quality in terms of Q-score as explained in the [fastq](#fastq) section.
6. CIGAR string. Describing which nucleotides were mapped, where insertions and deletions are and where mismatches occurs. For example, `43M1I10M3D18M` means that the first 43 nucleotides match with the reference genome, the next 1 nucleotide exists in the read but not in the reference genome (insertion), then 10 matches, then 3 nucleotides that do not exist in the read but do exist in the reference genome (deletions) and finally 18 matches. For more information see [this website](https://www.drive5.com/usearch/manual/cigar.html).
7. Reference name of the mate read (when using paired end datafiles). If no mate was mapped (e.g. in case of single end data or if it was not possible to map the mate read) this is typically set to `*`.
8. Position of the mate read. If no mate was mapped this is typically set to `0`.
9. Template length. Length of a group (i.e. mate reads or reads that are split up over multiple alignments) from the left most base position to the right most base position.
10. Nucleotide sequence.
11. Phred score of the sequence (see [fastq](#fastq) section).

Depending on the software, the sam file typically starts with a few header lines containing information regarding the alignment.
For example for BWA MEM (which is used in the pipeline), the sam file start with `@SQ` lines that shows information about the names and lengths for the different chromosome and `@PG` shows the user options that were set regarding the alignment software.
Note that these lines might be different when using a different alignment software.
Also, there is a whole list of optional fields that can be added to each read after the first 11 required fields.
For more information, see [wikipedia](https://en.wikipedia.org/wiki/SAM_(file_format)).

The flag in the sam files is a way of representing a list of properties for a read as a single integer.
There is a defined list of properties in a fixed order:

1. read paired
2. read mapped in proper pair
3. read unmapped
4. mate unmapped
5. read reverse strand
6. mate reverse strand
7. first in pair
8. second in pair
9. not primary alignment
10. read fails platform/vendor quality checks
11. read is PCR or optical duplicate
12. supplementary alignment

To determine the flag integer, a 12-bit binary number is created with zeros for the properties that are not true for a read and ones for those properties that are true for that read.
This 12-bit binary number is then converted to a decimal integer.
Note that the binary number should be read from right to left.
For example, FLAG=81 corresponds to the 12-bit binary 000001010001 which indicates the properties: 'read paired', 'read reverse strand' and 'first in pair'.
Decoding of sam flags can be done using [this website](http://broadinstitute.github.io/picard/explain-flags.html) or using [samflag.py](https://github.com/Gregory94/LaanLab-SATAY-DataAnalysis/blob/master/python_modules/samflag.py "LaanLab-SATAY_DataAnalysis.samflag.py").

Example sam file (note that the last read was not mapped):

>`NB501605:544:HLHLMBGXF:1:11101:25386:1198     2064    ref|NC_001136|  362539  0       42H34M  *       0       0       GATCACTTCTTACGCTGGGTATATGAGTCGTAAT      EEEAEEEEEEAEEEAEEAEEEEEEEEEEEAAAAA      NM:i:0  MD:Z:34 AS:i:34 XS:i:0  SA:Z:ref|NC_001144|,461555,+,30S46M,0,0;`
>
>`NB501605:544:HLHLMBGXF:1:11101:20462:1198       16      ref|NC_001137|  576415  0       75M     *       0       0       CTGTACATGCTGATGGTAGCGGTTCACAAAGAGCTGGATAGTGATGATGTTCCAGACGGTAGATTTGATATATTA     EEEAEEEEEEEEEEEEEAEEAE/EEEEEEEEEEEAEEEEEE/EEEEEAEAEEEEEEEEEEEEEEEEEEEEAAAAA     NM:i:1  MD:Z:41C33      AS:i:41 XS:i:41`
>
>`NB501605:544:HLHLMBGXF:1:11101:15826:1199       4       *       0       0       *       *       0       0       ACAATATTTGTGACTTATGTTATGCG      EEEEEEEEEEE6EEEEEEEEEEEEEE      AS:i:0  XS:i:0`

Sam files tend to be large in size (tens of Gb is normal).
Therefore the sam files are typically stored as compressed binary files called bam files.
Almost all downstream analysis tools (at least all tools discussed in this document) that need the alignment information accept bam files as input.
Therefore the sam files are mostly deleted after the bam file is created.
When a sam file is needed, it can always be recreated from the bam file, for example using `SAMTools` using the command `samtools view -h -o out.sam in.bam`.
The bam file can be sorted (creating a .sorted.bam file) where the reads are typically ordered depending on their position in the genome.
This usually also comes with an index file (a .sorted.bam.bai file) which stores some information where for example the different chromosomes start within the bam file and where specific often occuring sequences are.
Many downstream analysis tools require this file to be able to efficiently search through the bam file.

### bed

A bed file is one of the outputs from the transposon mapping pipeline.
It is a standard format for storing read insertion locations and the corresponding read counts.
The file consists of a single header, typically something similar to `track name=[file_name] userscore=1`.
Every row corresponds to one insertion and has (in case of the satay analysis) the following space delimited columns:

1. chromosome (e.g. `chrI` or `chrref|NC_001133|`)
2. start position of insertion
3. end position of insertion (in case of satay-analysis, this is always start position + 1)
4. dummy column (this information is not present for satay analysis, but must be there to satisfy the bed format)
5. number of reads at that insertion location

In case of processing with `transposonmapping.py` (final step in processing pipeline) or [the matlab code from the kornmann-lab](https://sites.google.com/site/satayusers/complete-protocol/bioinformatics-analysis/matlab-script), the number of reads are given according to `(reads*20)+100`, for example 2 reads are stored as 140.

The bed file can be used for many downstream analysis tools, for example [genome_browser](http://genome-euro.ucsc.edu/index.html).

Sometimes it might occur that insertions are stored outside the chromosome (i.e. the insertion position is bigger than the length of that chromosome).
Also, reference genomes sometimes do not have the different chromosomes stored as roman numerals (for example `chrI`, `chrII`, etc.) but rather use different names (this originates from the chromosome names used in the reference genome).
These things can confuse some analysis tools, for example the [genome_browser](http://genome-euro.ucsc.edu/index.html).
To solve this, the python function [clean_bedwigfiles.py](#clean_bedwigfilespy) is created.
This creates a _clean.bed file where the insertions outside the chromosome are removed and all the chromosome names are stored with their roman numerals.
See [clean_bedwigfiles.py](#clean_bedwigfilespy) for more information.

Example bed file:

> `track name=leila_wt_techrep_ab useScore=1`  
> `chrI 86 87 . 140`  
> `chrI 89 90 . 140`  
> `chrI 100 101 . 3820`  
> `chrI 111 112 . 9480`

### wig

A wiggle (wig) file is another output from the transposon mapping pipeline.
It stores similar information as the bed file, but in a different format.
This file has a header typically in the form of `track type=wiggle_0 maxheightPixels=60 name=[file_name]`.
Each chromosome starts with the line `variablestep chrom=chr[chromosome]` where `[chromosome]` is replaced by a chromosome name, e.g. `I` or `ref|NC_001133|`.
After a variablestep line, every row corresponds with an insertion in two space delimited columns:

1. insertion position
2. number of reads

In the wig file, the read count represent the actual count (unlike the bed file where an equation is used to transform the numbers).

There is one difference between the bed and the wig file.
In the bed file the insertions at the same position but with a different orientation are stored as individual insertions.
In the wig file these insertions are represented as a single insertion and the corresponding read counts are added up.

Similar to the bed file, also in the wig insertions might occur that have an insertion position that is bigger then the length of the chromosome.
This can be solved with the [same python script](#clean_bedwigfilespy) as the bed file.
The insertions that have a position outside the chromosome are removed and the chromosome names are represented as a roman numeral.

Example wig file:

> `track type=wiggle_0 maxheightPixels=60 name=WT_merged-techrep-a_techrep-b_trimmed.sorted.bam`  
> `variablestep chrom=chrI`  
> `86 2`  
> `89 2`  
> `100 186`  
> `111 469`

### pergene.txt, peressential.txt

A pergene.txt and peressential.txt file are yet another outputs from the transposon mapping pipeline.
Where bed and wig files store *all* insertions throughout the genome, these files only store the insertions in each gene or each essential gene, respectively.
Essential genes are the annotated essential genes as stated by SGD for wild type cells.
The genes are taken from the [Yeast_Protein_Names.txt](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Yeast_Protein_Names.txt) file, which is downloaded from [uniprot](https://www.uniprot.org/docs/yeast).
The positions of each gene are determined by a [gff3 file](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Saccharomyces_cerevisiae.R64-1-1.99.gff3) downloaded from SGD.
Essential genes are defined in [Cerevisiae_AllEssentialGenes.txt](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Cerevisiae_AllEssentialGenes_List.txt).

The pergene.txt and the peressential.txt have the same format.
This consists of a header and then each row contains three tab delimited columns:

1. gene name
2. total number of insertions within the gene
3. sum of all reads of those insertions

The reads are the actual read counts.
To suppress noise, the insertion with the highest read count in a gene is removed from that gene.
Therefore, it might occur that a gene has 1 insertion, but 0 reads.

Note that when comparing files that include gene names there might be differences in the gene naming.
Genes have multiple names, e.g. systematic names like 'YBR200W' or standard names like 'BEM1' which can have aliases such as 'SRO1'.
The above three names all refer to the same gene.
The [Yeast_Protein_Names.txt](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Yeast_Protein_Names.txt) file can be used to search for aliases when comparing gene names in different files. 

Example of pergene.txt file:

> `Gene name Number of transposons per gene Number of reads per gene`  
> `YAL069W 34 1819`  
> `YAL068W-A 10 599`  
> `PAU8 26 1133`  
> `YAL067W-A 12 319`

### pergene_insertions.txt, peressential_insertions.txt

The final two files that are created by the transposon mapping pipeline are the pergene_insertions.txt and the peressential_insertions.txt.
The files have a similar format as the pergene.txt file, but are more extensive in terms of the information per gene.
The information is taken from [Yeast_Protein_Names.txt](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Yeast_Protein_Names.txt), the [gff3 file](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Saccharomyces_cerevisiae.R64-1-1.99.gff3) and [Cerevisiae_AllEssentialGenes.txt](https://github.com/SATAY-LL/Transposonmapper/blob/main/transposonmapper/data_files/Cerevisiae_AllEssentialGenes_List.txt), similar as the pergene.txt files.

Both the pergene_insertions.txt and the peressential_insertions.txt files have a header and then each row contains six tab delimited columns:

1. gene name
2. chromosome where the gene is located
3. start position of the gene
4. end position of the gene
5. list of all insertions within the gene
6. list of all read counts in the same order as the insertion list

This file can be useful when not only the number of insertions is important, but also the distribution of the insertions within the genes.
Similarily as the pergene.txt and peresential.txt file, to suppress noise the insertion with the highest read count in a gene is removed from that gene.

- This file is uniquely created in the processing workflow described below.

- If the index file .bam.bai is not present, create this before running the python script.
The index file can be created using the command `sambamba-0.7.1.-linux-static sort -m 1GB [path]/[filename.bam]`.
This creates a sorted.bam file and a sorted.bam.bai index file.



Example of peressential_insertions.txt file:
> `EFB1 I 142174 143160 [142325, 142886] [1, 1]`  
> `PRE7 II 141247 141972 [141262, 141736, 141742, 141895] [1, 1, 1, 1]`  
> `RPL32 II 45978 46370 [46011, 46142, 46240] [1, 3, 1]`
