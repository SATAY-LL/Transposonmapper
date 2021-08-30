# Data analysis steps

For data analysis, the following steps need to be taken:

1. Process data and represent this in a standardized way that can be easily processed.

2. Put the genes in an overview for comparison with other backgrounds.
      - Make visual overview of the results (e.g. the number of insertions and reads per gene).
      - Compare the genes of different genetic backgrounds using a Venn-diagram

3. Obtain the interactions of the different genes to create an
    interaction map (use thecellmap.org)

4. Look for possible relations between the genes and their
    interactions.

5. Use these relations to obtain training for machine learning.

First, the main focus will be step 1 of the analysis (see next section).

## Step 1 data analysis; From raw data to essential protein overview

SATAY experiments need to be sequenced which results in a FASTQ file.
The sequence reads from this file needs to be aligned to create a SAM file (and/or the compressed {bash}ary equivalent BAM file).
Using the BAM file, the number of transposons can be determined for each insertion location.

For guides and manuals of the software discussed below, see the folder

`M:\\tnw\\bn\\ll\\Shared\\Gregory\\Software\\Guides & Manuals`.

Raw data (.FASTQ file) discussed in the paper of Michel et.al. 2017 can be found at [<https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-4885/samples/>].

## Workflow

The results from the sequencing is typically represented in FASTA or FASTQ format.
This needs to be aligned according to a reference sequence to create a SAM and BAM file.
Before alignment, the data needs to be checked for quality and possibly trimmed to remove unwanted and unnecessary sequences.
When the location of the reads relative to a reference sequence are known, the insertion sites of the transposons can be determined.
With this, a visualization can be made that shows the number of transposon insertions per gene.

In the description given in this document, it is chosen to do the quality checking and the trimming in windows and the alignment of the reads with a reference genome in a virtual machine running Linux.
It is possible to do the quality checking and trimming in Linux as well or to do the whole process in windows.
To do quality checking and/or trimming in Linux requires more memory of the Linux machine since both the raw sequencing data needs to be stored and the trimming needs to be stored (both which can be relatively large files).
Since a virtual machine is used, both the computation power and the amount of storage is limited, and therefore it chosen to do the trimming on the main windows computer (this problem would not exists if a computer is used running on Linux, for example a computer with an alternative startup disc running Linux).
Sequence alignment can be done on Windows machines (e.g. using [BBmap](https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbmap-guide/)), but this is not ideal as many software tools are designed for Unix based computer systems (i.e. Mac or Linux).
Also, many tools related to sequence alignment (e.g. converting .sam files to .bam and sorting and indexing the bam files) are done with tools not designed to be used in windows, hence this is performed in Linux.

An overview of the different processing steps are shown in the figure below.

![Processing pipeline. Input is a file containing the raw reads from the sequencing saved in a .fastq file.](./media/processing_pipeline.png)

A short overview is given for different software tools that can be used for processing and analyzing the data.
Next, a step-by-step tutorial is given as an example how to process the data.
Most of this is done using command line based tools.

An overview of the different steps including some software that can handle this is shown here:

1. Checking the raw FASTA or FASTQ data can be done using the
    ([**FASTQC**](<https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>)) software (Windows, Linux, Mac. Requires Java).
    This gives a quality report (see accompanying tutorial) for the sequence reads and can be run non-interactively using the command line.

2. Based on the quality report, the data needs to be trimmed to remove any unwanted sequences.
    This can be done with for example ([**FASTX**](<http://hannonlab.cshl.edu/fastx_toolkit/index.html>)) (Linux, Mac) or ([**Trimmomatic**](<http://www.usadellab.org/cms/?page=trimmomatic>)) (Windows,requires Java).
    An easy graphical user interface that com{bash}es the FASTQC and Trimmomatic is ([**123FASTQ**](<https://sourceforge.net/projects/project-123ngs/>)).
    Also **BBDuk** can be used for trimming (which belongs to BBMap).

3. The trimmed sequence reads need to be aligned using a reference
    sequence, for example the *S. Cerevisiae* [S288C Ref64-2-1 reference sequence](<https://downloads.yeastgenome.org/sequence/S288C_reference/>) or the [W303 reference sequence](<http://sgd-archive.yeastgenome.org/sequence/strains/W303/W303_SGD_2015_JRIU00000000/>) from SGD.
    Aligning can be done, for example, using ([**SnapGene**](<https://www.snapgene.com/>)) (Windows, Linux, Mac. This does not
    import large files and is therefore not suitable for whole genome
    sequencing), ([**BBMap**](<https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbmap-guide/>)) (Linux, Mac, Windows (seems to give problems when installing on windows machines), might be possible to integrate it in Python, ([**BWA**](<http://bio-bwa.sourceforge.net/>)) (Linux, Mac), ([**Bowtie2**](<http://bowtie-bio.sourceforge.net/bowtie2/index.shtml>)) (Linux, Mac) or ([**ClustalOmega**](<http://www.clustal.org/omega/>)) (Windows, Linux, Mac).
    This step might require defining scores for matches, mismatches, gaps and insertions of nucleotides.

4. After aligning, the data needs to be converted to SAM and BAM formats for easier processing hereafter.
    This requires ([**SAMtools**](<http://www.htslib.org/>)) (Linux, Mac) or ([**GATK**](<https://gatk.broadinstitute.org/hc/en-us>)) (Linux, Mac).
    Conversion from SAM to BAM can also be done in Matlab if preferred using the ‘BioMap’ function.

5. Using the BAM file with the aligned sequence reads, the transposon insertion sites can be determined using the [**Matlab** script given by Benoit Kornmann Lab](<https://sites.google.com/site/satayusers/>) (including the name.mat and yeastGFF.mat files).
    The results from this step are three files (a .txt file, a .bed file and a .wig file) that can be used for visualization.

6. If more processing is required, ([**Picard**](<https://broadinstitute.github.io/picard/>)) (Linux, Mac) might be useful, as well as ([**GATK**](<https://gatk.broadinstitute.org/hc/en-us>)) (Linux, Mac).
    Visualization of the genomic dataset can be done using ([**IGV**](<https://software.broadinstitute.org/software/igv/home>)) (Windows, Linux, Mac) or SAMtools’ tview function.
    Also ([**sambamba**](<https://lomereiter.github.io/sambamba/>)) (Linux, Mac) can be used, especially for sorting and indexing the bam files.

7. Creating transposon insertion maps for the genome (see the [satay users website](<https://sites.google.com/site/satayusers/>)) and comparison essential genes between different genetic backgrounds using Venn diagrams, customized software needs to be created.

### Initializing

The steps discussed in this section are not obligatory, but might help in organizing the data.
The **bold** printed commands in this and the following sections are put so that they can be copied directly to the {bash}.
(Note to modify the respective paths on your own machine in this Initialization step, though).
If the paths below are correctly defined, the boldface commands defined in the different processing steps below can be literally copied and pasted in the {bash}.

Since this protocol works mostly in the Linux Virtual Machine, the commands below are defined for Linux.
First, a possible method for organizing the data is shown, but feel free to change this as you like.

1. Create an empty datafolder.

2. Add the .fastq file to the datafolder.

3. Add the following empty folders for the outcomes of the different processing steps:

    A. filename_QC

    B. filename_Trimmed

    C. filename_Aligned

4. When this is done in Windows, copy the datafolder to the shared folder for processing in the Virtual Machine using the commands (using git-{bash})

Considering that :

**`pathwin_sharedfolder='/C/Users/gregoryvanbeek/Documents/ VirtualBox VMs/ VMSharedFolder_Ubuntu64_1'`**

**`pathwin_data='C:\Users\gregoryvanbeek\Desktop\Cerevisiae_WT2_Seqdata_Michel2017\Cerevisiae_WT2_Seqdata_Michel2017_ProcessingTest'`**

```{bash}

cp -r ${pathwin_data} "${pathwin_sharedfolder}"
```

5. The main processing is done in the Linux Virtual Machine.
Since the software tools are mostly commandline based, it might be convenient to be able to define variables, for example for the paths to the difference programs and files so that these do not have te be entered every single time.
For this start with the command that enables defining variables **`#!/{bash}/{bash}`**.

6. Define the following variables. (copy paste the commands in the {bash} using `shift+Ins`. Remember to first alter the respective variables given below to the paths and filenames in your computer):

    A. Path to the shared folder used for communicating with the virtual machine running Linux (**`path_sf=/media/sf_VMSharedFolder_Ubuntu64_1/`**).

    B. Name of the folder containing the data
    (**`foldername='Cerevisiae_WT2_Seqdata_ Michel2017_ProcessingTest'`**)

    C. Name of the data file
    (**`filename='Cerevisiae_WT2_Michel2017.fastq'`**)

    D. Name of the trimmed data file
    (**`filename_trimmed='Cerevisiae_WT2_Michel2017_trimmed.fastq'`**)

    D. The processing can be performed in shared folder, but this is not recommended.
    It is better to move the folder temporarily to the hard drive of the Virtual Machine.
    For this define the location where the processing is performed (in this example located in the Documents directory)
    (**`pathdata=~/Documents/data_processing/${foldername}`**)
    If this directory does not already exists, create it using the command `mkdir ${pathdata}`

    E. Move the datafolder from shared folder to data processing folder
    (**`mv ${path_sf}${foldername} ${pathdata}`**)

    F. Path to the location where the Trimmomatic software is located
    (**`path_trimm_software=~/Documents/ Software/Trimmomatic-0.39/`**).

    G. Path to the location where the BBDuk software is located
    (**`path_bbduk_software=~/Documents/ Software/BBMap/bbmap/`**)

    H. Path to the outcome folder for the fastqc software
    (**`path_fastqc_out=${pathdata}/ Cerevisiae_WT2_Michel2017_QC/`**).

    I. Path to the outcome folder for the trimmomatic software
    (**`path_trimm_out=${pathdata}/ Cerevisiae_WT2_Michel2017_Trimmed/`**).

    J. Path to the outcome folder for the aligned software
    (**`path_align_out=${pathdata}/ Cerevisiae_WT2_Michel2017_Aligned/`**).

    K. Path to the reference genome fasta file
    (**`path_refgenome=/home/gregoryvanbeek/Documents/
    Reference_Sequences/Reference_Sequence_S288C/S288C_reference_sequence_R64-2-1_20150113.fsa`**)

Some useful commands:

1. `echo`: Print a variable name or some text.

2. `gunzip`: Unzip a .gz file.

3. `bunzip`: Unzip a .bz file.

4. `${}`: when using a variable, the name of the variable should be placed between curly brackets and should start with a dollar sign (`$`), otherwise the {bash} won't recognize the name as a variable.

5. `less`: open the first few lines of a files that can be read as a text file.

6. When using or defining strings of texts, putting the string between accolades ('') tells the {bash} to take the text within the accolades literally.
Remember this when using the variables, as `'${var}'` is literally taken as the string ${var} whereas when using `${var}` (without accolades) the {bash} will try implement the variable 'var' depending on what you have defined before for this variable.

7. Copying texts in the {bash} does not work using `crtl-v`, instead use `shift-Insert`

A suggestion is to put all the commands with the correct paths in a text file and store this text file together with the raw sequencing file ('Linux_Processing_Commands.txt' located at the [SATAY github repository](https://github.com/Gregory94/LaanLab-SATAY-DataAnalysis/blob/dev_Gregory/docs/Linux_Processing_Commands.txt)).
The variables containing the paths and names in this file can be changed to point at the right files and directories in your computer.
Then all the commands can be easily copy-pasted in the {bash} and all the processing steps can be traced back later using this text file.

### 1. Quality checking of the sequencing reads; FASTQC (0.11.9)

FASTQC creates a report for the quality of sequencing data.
The input should be a fastq (both zipped and unzipped), sam or bam file (it can handle multiple files at once).
The program does not need to be installed, but after downloading only requires to be unzipped.
FASTQC can be ran as an interactive program (i.e. using a GUI) or non-interactively using the command line options.

If using interactively, open the ‘run\_fastqc.bat’ file in the FASTQC folder and load a file to be checked. Alternatively using the 123FASTQ (version 1.1) program, open this and use the ‘Quality Check’ menu on the right.
The advantage of using 123FASTQ is that it can also do trimming (using Trimmomatic).

If using the command line for checking a single file use the command:

```{bash}

fastqc --outdir ${path_fastqc_out} ${pathdata}/${filename}
```

(Note that the output directory should already exist, as the program does not create directories).
In the output directory, a .html file and a (zipped) folder is created, both with the same name as the input file.
The .html file can be used to quickly see the graphs using a browser.
Also, a zipped folder is created where the raw data of the quality check is stored.
For explanation about the different graphs, see the fastqc\_manual pdf or [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/] (or the paper ‘Preprocessing and Quality Control for Whole-Genome’ from Wright et.al. or the ‘Assessing Read Quality’ workshop from the Datacarpentry Genomics workshop).

For more commands, type `fastqc --help`.
Some useful commands might be:

- --contaminants Reads a file where sequences are stored of (potential) contaminants.
    The .txt-file should be created before running the software.
    Each contaminant is presented on a different line the text file and should have the form name 'tab' sequence.

- --adapters Similar as the contaminants command, but specifically for adapter sequences.
    Also here a text file should be created before running and this file should have the same layout as the contaminants file.

- --min_length where a minimal sequence length can be set, so that the statistics can be better compared between different reads of different length (which for example might occur after trimming).

- --threads Preferably leave this unchanged, especially when an error is shown that there ‘could not reserve enough space for object heap’ after setting this command.

- --extract Set this command (without following of parameters) to extract the zipped folder from the results.

The output of the FASTQC program is:

- **Per base sequence quality**: Box and whisker plot for the quality of a basepair position in all reads.
The quality should be above approximately 30 for most reads, but the quality typically drops near the end of the sequences.
If the ends of the reads are really bad, consider trimming those in the next step.

- **Per tile sequence quality**: (Shows only when Illumina Library which retains there sequence identifier).
Shows a heat map of the quality per tile of the sequence machines.
Blueish colours indicate that the quality score is about or better than average and reddish colours indicates scores worse than average.

- **Per sequence quality score**: Shows an accumulative distribution to indicate which mean quality score per sequence occurs most often.

- **Per base sequence content**: Shows the percentage of nucleotide appearance in all sequences.
Assuming a perfectly random distribution for all four nucleotides, each nucleotide should be present about 25% over the entire sequence. In the beginning this might be a bit off due to for example adapters present in the sequences.
If this is present, it might difficult/impossible to cut these during the trimming part, but it should typically not seriously affect further analysis.

- **Per sequence GC content**: Indicates the distribution of the G-C nucleotides appearances in the genome.
The ideal distribution that is expected based on the data is shown as a blue curve.
The red curve should, ideally follow the blue curve.
If the red curve is more or less a normal distribution, but shifted from the blue curve, is might indicate a systematic bias which might be caused by an inaccurate estimation of the GC content in the blue curve.
This does not necessarily indicate bad data.
When the red curve is not normal or show irregularities (peaks or flat parts), this might indicate contaminants in the sample or overrepresented sequences.

- **Per base N content**: Counts the number of N appearances in the data for each basepair position of all reads.
Every time a nucleotide cannot be accurately determine during sequencing, it is flagged with a N (No hit) in the sequence instead of one of the nucleotides.
Ideally this should never occur in the data and this graph should be a flat line at zero over the entire length.
Although at the end of the sequences it might occur few times, but it should not occur more than a few percent.

- **Sequence length distribution**: Shows the length of all sequences.
    Ideally all reads should have the same length, but this might change, for example, after trimming.

- **Sequence duplication level**: Indicates how often some sequences appear the data.
Ideally, all reads occur only few times and a high peak is expected near 1.
If peaks are observed at higher numbers, this might indicate enrichment bias during the sequencing preparation (e.g. over amplification during PCR).
Only the first 100000 sequences are considered and when the length of the reads is over 75bp, the reads are cut down to pieces of 50bp.
Some duplication might not be bad and therefore a warning or error here does not need to concern.

- **Overrepresented sequences**: List of sequences that appear in more 0.1% of the total (this is only considered for the first 100000 sequences and reads over 75bp are truncated to 50bp pieces).
The program gives a warning (when sequences are found to be present between 0.1% and 1% of the total amount of sequences) or an error (when there are sequences occurring more 1% of all sequences), but this does not always mean that the data is bad and might be ignored.
For Illumina sequencing for satay experiments, the sequences often start with either 'CATG' or 'GATC' which are the recognition sites for NlaIII and DpnII respectively.

- **Adapter content**: Shows an accumulative percentage plot of repeated sequences with a positional bias appearing in the data.
So if many reads have the same sequence at (or near) the same location, then this might trigger a warning in this section.
Ideally this is a flat line at zero (meaning that there are no repeated sequences present in the data).
If this is not a flat line at zero, it might be necessary to cut the reported sequences during the trimming step.
If this section gives a warning, a list is shown with all the repeated sequences including some statistics.
It can be useful to delete these sequences in the trimming step.

- **Kmer content**: indicates sequences with a position bias that are ofen repeated.
If a specific sequence occurs at the same location (i.e. basepair number) in many reads, then this module will show which sequence at which location turns up frequently.
Note that in later editions (0.11.6 and up) this module is by default turned off.
If you want to turn this module on again, go to the Configuration folder in the Fastqc folder and edit the limits.txt file in the line where it says 'kmer  ignore  1' and change the 1 in a 0.

### 2. Trimming of the sequencing reads

Next is the trimming of the sequencing reads to cut out, for example, repeated (adapter) sequences and low quality reads.
There are two software tools adviced, Trimmomatic and BBDuk.
Trimmomatic is relative simple to use and can be used interactively together with FASTQC.
However, the options can be limiting if you want more control over the trimming protocol.
An alternative is BBDuk, which is part of the BBMap software package.
This allows for more options, but can therefore also be more confusing to use initially.
Both software packages are explained below, but only one needs to be used.
Currently, it is advised to use BBDuk (see section 2b).

For a discussion about trimming, see for example the discussion in [MacManes et.al. 2014](https://www.frontiersin.org/articles/10.3389/fgene.2014.00013/full), [Del Fabbro et.al. 2013](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0085024) or [Delhomme et. al. 2014](https://pdfs.semanticscholar.org/daa6/191f2a91a1bd5008f2bda068ae3f99ec85fd.pdf) or at [basepairtech.com](https://www.basepairtech.com/blog/trimming-for-rna-seq-data/#:~:text=Quality%20trimming%20decreases%20the%20overall,useful%20data%20for%20downstream%20analyses.&text=Too%20aggressive%20quality%20trimming%20can,%2C%20estimation%20of%20gene%20expression) (although this discussion is on RNA, similar arguments hold for DNA sequence analysis).

#### 2a. Trimming of the sequencing reads; Trimmomatic (0.39)

Trimmomatic alters the sequencing result by trimming the reads from unwanted sequences, as is specified by the user.
The program does not need to be installed, but after downloading only requires to be unzipped.
Trimmomatic can be ran as an interactive program (for this 123FASTQ needs to be used) or non-interactively using the command line options.

If using interactively, use 123FASTQ (version 1.1) and run the ‘Runner.bat’ file in the 123FASTQ folder.
Use the ‘Trimmer’ in the ‘Trim Factory’ menu on the right.

If using non-interactively in the command line use the command:

```{bash}

java -jar ${path_trimm_software}'trimmomatic-0.39.jar'

```

Before running Trimmomatic, a .fasta file needs to be created that allows clipping unwanted sequences in the reads.
For example, the 'overrepresented sequences' as found by Fastqc can be clipped by adding the sequences to the .fasta file.
Easiest is to copy an existing .fasta file that comes with Trimmomatic and adding extra sequences that needs to be clipped.
For MiSeq sequencing, it is advised to use the TruSeq3 adapter file that needs to be copied to the data folder (see below for detailed explanation).
For this use the command:

```{bash}
 cp ${path_trimm_software}'adapters/''TruSeq3-SE.fa' ${pathdata}
```

Open the .fa file and copy any sequences in the file using a similar style as the sequences that are already present.
Typically it is useful to clip overrepresented sequences that start with 'CATG' or 'GATC' which are the recognition sites for NlaIII and DpnII respectively.
Note that the trimming is performed in the order in which the steps are given as input.
Typically the adapter clipping is performed as one of the first steps and removing short sequences as one of the final steps.

A typical command for trimmomatic looks like this:

```{bash}
java -jar ${path_trimm_software}'trimmomatic-0.39.jar' SE -phred33 ${pathdata}${filename} ${path_trimm_out}${filename_trimmed} ILLUMINACLIP:'TruSeq3-SE.fa':2:30:10 LEADING:14 TRAILING:14 SLIDINGWINDOW:10:14 MINLEN:30
```

Check the quality of the trimmed sequence using the command:

```{bash}
${path_fastqc_software}fastqc --outdir ${path_fastqc_out} ${path_trimm_out}${filename_trimmed}
```

The following can be set to be set by typing the following fields after the above command (the fields must be in the given order, the optional fields can be ignored if not needed, see also <http://www.usadellab.org/cms/?page=trimmomatic>):

- `SE` (Single End) or `PE` (Paired End) [required];

- `-phred33` or `-phred64` sets which quality coding is used, if not specified the program tries to determine this itself which might be less accurate.
usually the phred33 coding is used.
If not sure, check if the .fastq file contains, for example, an exclamation mark (!), a dollar sign ($), an ampersand (&) or any number (0-9) since these symbols only occur in the phredd33 coding and not in the phred64 coding [optional];

- `Input filename`. Both forward and reverse for paired end in case of PE [required];

- `Output filename`. Both paired and unpaired forward and paired and unpaired reverse for paired end (thus 4 output in total) in case of PE.
In case of SE, a single output file needs to be specified.
Needs to have the same extension as the input file (e.g. .fastq) [required];

- `ILLUMINACLIP:TruSeq3-SE.fa:2:15` or `ILLUMINACLIP:TruSeq3-PE.fa:2:30:10` (for Single End reads or Paired End reads respectively). This cuts the adapter and other Illumina specific sequences from the reads.
The first parameter after `:` indicates a FASTA file (this should be located in the same folder as the sequencing data).
The second paramter indicates the Seed Mismatches which indicates the maximum mismatch count that still allows for a full match to be performed.
The third parameter (for SE, fourth parameter for PE) is the Simple Clip Threshold which specifies how accurate the match between the adapter and the read.
The third parameter for PE sets the Palindrome Clip Threshold specifies how accurate the match between the two 'adapter
ligated' reads must be for PE palindrome read alignment.

A number of adapters are stored in the ‘adapters’ folder at the location where the trimmomatic program is saved.
In case of MiSeq sequencing, the TruSeq3 adapter file is advised.
The way the adapter sequences are aligned is by cutting the adapters (in the FASTA file) into 16bp pieces (called seeds) and these seeds are aligned to the reads.
If there is a match, the entire alignment between the read and the complete adapter sequence is given a score.
A perfect match gets a score of 0.6.
Each mismatching base reduces the score by Q/10.
When the score exceeds a threshold, the adapter is clipped from the read. The first number in the parameter gives the maximal number of mismatches allowed in the seeds (typically 2).
The second value is the minimal score before the adapter is clipped (typically between 7 (requires $\frac{7}{0.6}=12$ perfect matches) and 15 (requires $\frac{15}{0.6}=25$ perfect matches)).
High values for short reads (so many perfect matches are needed) allows for clipping adapters, but not for adapter contaminations.
Note a bug in the software is that the FASTA file with the adapters need to be located in your current folder.
A path to another folder with the adapter files yields an error. [optional] [<https://wiki.bits.vib.be/index.php/Parameters_of_Trimmomatic>];

- `SLIDINGWINDOW` Sliding window trimming which cuts out sequences witin the window and all the subsequent basepairs in the read if the average quality score within the window is lower than a certain threshold.
The window moves from the 5'-end to the 3'-end.
Note that if the first few reads of a sequence if of low quality, but the remaining of the sequence is of high quality, the entire sequence will be removed just because of the first few bad quality nucleotides.
If this sitatuation occurs, it might be useful to first apply the HEADCROP option (see below).
Parameters should be given as `SLIDINGWINDOW:L_window:Q_min` where `L_window` is the window size (in terms of basepairs) and `Q_min` the average threshold quality. [optional];

- `LEADING` Cut the bases at the start (5’ end) of a read if the quality is below a certain threshold. Note that when, for example, the parameter is set to 3, the quality score Q=0 to Q=2 will be removed.
Parameters should be given as `LEADING:Q_min` where `Q_min` is the threshold quality score.
All basepairs will be removed until the first basepair that has a quality score above the given threshold. [optional];

- `TRAILING` Cut the bases at the end (3’ end) of a read if the quality is below a certain threshold. Note that when, for example, the parameter is set to 3, the quality score Q=0 to Q=2 will be removed.
All basepairs will be removed until the first basepair that has a quality score above the given threshold. [optional];

- `CROP` Cuts the read to a specific length by removing a specified amount of nucleotides from the tail of the read (this does not discriminate between quality scores). [optional];

- `HEADCROP` Cut a specified number of bases from the start of the reads (this does not discriminate between quality scores). [optional];

- `MINLEN` Drops a read if it has a length smaller than a specified amount [optional];

- `TOPHRED33` Converts the quality score to phred33 encoding [optional];

- `TOPHRED64` Converts the quality score to phred64 encoding [optional].

Note that the input files can be either uncompressed FASTQ files or gzipped FASTQ (with an extension fastq.gz or fq.gz) and the output fields should ideally have the same extension as the input files (i.e. .fastq or .fq).
The convention is using field:parameter, where ‘parameter’ is typically a number.
(To make the (relative long commands) more readable in the command line, use \\ and press enter to continue the statement on the next line) (See ‘Datacarpentry workshop > data Wrangling and Processing for Genomics > Trimming and Filtering’ for examples how to run software).
Trimmomatic can only run a single file at the time.
If more files need to be trimmed using the same parameters, use

```{bash}
for infile in *.fastq
  do
  base=$(basename $(infile) .fastq)
  trimmomatic xxx
done
```

Where `xxx` should be replaced with the commands for trimmomatic.

#### 2b. Trimming of the sequencing reads; BBDuk (38.84)

BBDuk is part of the BBMap package and alters the sequencing result by trimming the reads from unwanted sequences, as is specified by the user.
The program does not need to be installed, but after downloading only requires to be unzipped.

Before running BBDuk, a .fasta file can to be created that allows clipping unwanted sequences in the reads.
For example, the 'overrepresented sequences' as found by Fastqc can be clipped by adding the sequences to the .fasta file.
A .fasta file can be created by simply creating a text file and adding the sequences that need to be clipped, for example, in the form:

> \> Sequence1
>
> CATG
>
> \> Sequence2
>
> GATC

Or a .fasta can be copied from either Trimmomatic software package or the BBDuk package, both which are provided with some standard adapter sequences.
In the case of Trimmomatic it is advised to use the TruSeq3 adapter file when using MiSeq sequencing.
To copy the .fasta file to the data folder (see below for detailed explanation) use the following command:

```{bash}

 cp ${path_trimm_software}'adapters/''TruSeq3-SE.fa' ${pathdata}

```

When using the adapter file that comes with BBMap, use the command:

```{bash}

cp ${path_bbduk_software}'resources/adapters.fa' ${pathdata}
```

The adapters.fa file from the BBDuk package includes many different adapter sequences, so it might be good to remove everything that is not relevant.
One option can be to create a custom fasta file where all the sequences are placed that need to be trimmed and save this file in the bbmap/resources folder.
To do this, in order to let everything work properly it is best to alter one of the existing .fa files.
First copy that file as a backup using a different name (e.g. in the `#{path_bbduk_software}/resources` directory type the command `cp adapters.fa adapters_original_backup.fa`).
Then, alter the adapters.fa file with any sequences you want to get trimmed.
Note to not put empty lines in the text file, otherwise BBDuk might yield an error about not finding the adapters.fa file.

Typically it is useful to clip overrepresented sequences that were found by FASTQC and sequences that start with 'CATG' or 'GATC' which are the recognition sites for NlaIII and DpnII respectively.
Note that the trimming is performed in the order in which the steps are given as input.
Typically the adapter clipping is performed as one of the first steps and removing short sequences as one of the final steps.

BBDuk uses a kmers algorithm, which basically means it divides the reads in pieces of length k.
(For example, the sequence 'abcd' has the following 2mers: ab,bc,cd).
For each of these pieces the software checks if it contains any sequences that are present in the adapter file.
The kmers process divides both the reads and the adapters in pieces of length k and it then looks for an exact match.
If an exact match is found between a read and an adapter, then that read is trimmed.
If the length k is chosen to be bigger than the length of the smallest adapter, then there will never be an exact match between any of the reads and the adapter sequence and the adapter will therefore never be trimmed.
However, when the length k is too small the trimming might be too specific and it might trim too many reads.
Typically, the length k is chosen about the size of the smallest adapter sequence or slighty smaller.
For more details, see [this webpage](https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/).

A typical command for BBDuk looks like this:
**`${path_bbduk_software}/bbduk.sh -Xmx1g in=${pathdata}/${filename} out=${path_trimm_out}${filename_trimmed} ref=${path_bbduk_software} /resources/adapters.fa ktrim=r k=23 mink=10 hdist=1 qtrim=r trimq=14 minlen=30`**

Next an overview is given with some of the most useful options.
For a full overview use call `bbduk.sh` in the {bash} without any options.

1. `-Xmx1g`. This defines the memory usage of the computer, in this case 1Gb (`1g`).
Setting this too low or too high can result in an error (e.g. 'Could not reserve enough space for object heap').
Depending on the maximum memory of your computer, setting this to `1g` should typically not result in such an error.
2. `in` and `out`. Input and Output files.
For paired-end sequencing, use also the commands `in2` and `out2`.
The input accepts zipped files, but make sure the files have the right extension (e.g. file.fastq.gz).
Use `outm` (and `outm2` when using paired-end reads) to also save all reads that failed to pass the trimming.
Note that defining an absolute path for the path-out command does not work properly.
Best is to simply put a filename for the file containing the trimmed reads which is then stored in the same directory as the input file and then move this trimmed reads file to any other location using:
`mv ${pathdata}${filename::-6}_trimmed.fastq ${path_trimm_out}`
3. `qin`. Set the quality format.
33 for phred 33 or 64 for phred 64 or auto for autodetect (default is auto).
4. `ref`. This command points to a .fasta file containg the adapters.
This should be stored in the location where the other files are stored for the BBDuk software (`${path_bbduk_software}/resources`)
Next are a few commands relating to the kmers algorithm.
5. `ktrim`. This can be set to either don't trim (`f`, default), right trimming (`r`), left trimming (`l`).
Basically, this means what needs to be trimmed when an adapter is found, where right trimming is towards the 5'-end and left trimming is towards the 3'-end.
For example, when setting this option to `ktrim=r`, then when a sequence is found that matches an adapter sequence, all the basepairs on the right of this matched sequence will be deleted including the matched sequence itself.
When deleting the whole reads, set `ktrim=rl`.
6. `kmask`. Instead of trimming a read when a sequence matches an adapter sequence, this sets the matching sequence to another symbol (e.g. `kmask=N`).
7. `k`. This defines the number of kmers to be used. This should be not be longer than the smallest adapter sequences and should also not be too short as there might too much trimmed. Typically values around 20 works fine (default=27).
8. `mink`. When the lenght of a read is not a perfect multiple of the value of `k`, then at the end of the read there is a sequence left that is smaller than length k. Setting `mink` allows the software to use smaller kmers as well near the end of the reads.
The sequence at the end of a read are matched with adapter sequences using kmers with length between mink and k.
9. `minkmerhits`. Determines how many kmers in the read must match the adapter sequence.
Default is 1, but this can be increased when for example using short kmers to decrease the chance that wrong sequences are trimmed that happen to have a single matching kmer with an adapter.
10. `minkmerfraction`. A kmer in this read is considered a match with an adapter when at least a fraction of the read matches the adapter kmer.
11. `mincovfraction`. At least a fraction of the read needs to match adapter kmer sequences in order to be regarded a match.
Use either `minkmerhits`, `minkmerfraction` or `mincovfraction`, but setting multiple results in that only one of them will be used during the processing.
12. `hdist`. This is the Hamming distance, which is defined as the minimum number of substitutions needed to convert one string in another string.
Basically this indicates how many errors are allowed between a read and and an adapter sequence to still count as an exact match.
Typically does not need to be set any higher than 1, unless the reads are of very low quality.
Note that high values of hdist also requires much more memory in the computer.
13. `restrictleft` and `restrictright`. Only look for kmers left or right number bases.
14. `tpe` and `tbo`: This is only relevant for paired-end reads.
`tpe` cuts both the forward and the reverse read to the same length and `tbo` trims the reads if they match any adapter sequence while considering the overlap between two paired reads.

So far all the options were regarding the adapter trimming (more options are available as well, check out the [user guide](https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/)).
These options go before any other options, for example the following:

15. `qtrim`. This an option for quality trimming which indicates whether the reads should be trimmed on the right (`r`), the left (`l`), both (`fl`), neither (`f`) or that a slidingwindow needs to be used (`w`).
The threshold for the trimming quality is set by `trimq`.
16. `trimq`. This sets the minimum quality that is still allowed using phred scores (e.g. Q=14 corresponds with $P_{error} = 0.04$).
17. `minlength`. This sets the minimum length that the reads need to have after all previous trimming steps.
Reads short than the value given here are discarded completely.
18. `mlf`. Alternatively to the `minlen` option, the Minimum Length Fraction can be used which determines the fraction of the length of the read before and after trimming and if this drops below a certain value (e.g 50%, so `mlf=50`), then this read is trimmed.
19. `maq`. Discard reads that have an average quality below the specified Q-value.
This can be useful after quality trimming to discard reads where the really poor quality basepairs are trimmed, but the rest of the basepairs are of poor quality as well.
20. `ftl` and `ftr` (`forcetrimleft` and `forcetrimright`). This cuts a specified amount of basepairs at the beginning (`ftl`) or the last specified amount of basepairs (`ftr`).
Note that this is zero based, for example `ftl=10` trims basepairs 0-9.
21. `ftm`. This force Trim Modulo option can sometimes be useful when an extra, unwanted and typically very poor quality, basepair is added at the end of a read.
So when reads are expected to be all 75bp long, this will discard the last basepair in 76bp reads.
When such extra basepairs are present, it will be noted in FastQC.

Finally, to check the quality of the trimmed sequence using the command:

```{bash}

fastqc --outdir ${path_fastqc_out} ${path_trimm_out}/${filename_trimmed}
```

### 3. Sequence alignment and Reference sequence indexing; BWA (0.7.17) (Linux)

The alignment can be completed using different algorithms within BWA, but the ‘Maximal Exact Matches’ (MEM) algorithm is the recommended one (which is claimed to be the most accurate and fastest algorithm and is compatible with many downstream analysis tools, see [documentation](http://bio-bwa.sourceforge.net/bwa.shtml) for more information).
BWA uses a FM-index, which uses the Burrows Wheeler Transform (BWT), to exactly align all the reads to the reference genome at the same time.
Each alignment is given a score, based on the number of matches, mismatches and potential gaps and insertions.
The highest possible score is 60, meaning that the read aligns perfectly to the reference sequence (this score is saved in the SAM file as MAPQ).
Besides the required 11 fields in the SAM file, BWA gives some optional fields to indicate various aspects of the mapping, for example the alignment score (for a complete overview and explanation, see the [documentation](http://bio-bwa.sourceforge.net/bwa.shtml)).
The generated SAM file also include headers where the names of all chromosomes are shown (lines starting with SQ).
These names are used to indicate where each read is mapped to.

Before use, the reference sequence should be indexed so that the program knows where to find potential alignment sites.
This only has to be done *once* for each reference genome.
Index the reference genome using the command

```{bash}
bwa index /path/to/reference/sequence/file.fasta
```

This creates 5 more files in the same folder as the reference genome that BWA uses to speed up the process of alignment.

The alignment command should be given as

```{bash}

bwa mem [options] ${path_refgenome} ${path_trimm_out}${filename_trimmed} > ${path_align_out} ${filename_trimmed::-6}'.sam'
```

where `[options]` can be different statements as given in the
documentation. Most importantly are:

- `-A` Matching scores (default is 1)

- `-B` Mismatch scores (default is 4)

- `-O` Gap open penalty (default is 6)

- `-E` Gap extension penalty (default is 1)

- `-U` Penalty for unpaired reads (default is 9; only of use in case of paired-end sequencing).

Note that this process might take a while.
After BWA is finished, a new .sam file is created in the same folder as the .fastq file.

### 4. Converting SAM file to BAM file; SAMtools (1.7) and sambamba (0.7.1) (Linux)

SAMtools allows for different additional processing of the data. For an overview of all functions, simply type samtools in the command line. Some useful tools are:

- `view` This converts files from SAM into BAM format. Enter samtools view to see the help for all commands. The format of the input file is detected automatically. Most notably are:

  - `–b` which converts a file to BAM format.

  - `–f` int Include only the reads that include all flags given by
        int.

  - `–F` int Include only the reads that include none of the flags
        given by int.

  - `–G` int Exclude only the reads that include all flags given by
        int.

- `sort` This sorts the data in the BAM file. By default the data is
    sorted by leftmost coordinate. Other ways of sorting are:

  - `–n` sort by read name

  - `–t` tag Sorts by tag value

  - `–o` file Writes the output to file.

- `flagstats` Print simple statistics of the data.

- `stats` Generate statistics.

- `tview` This function creates a text based Pileup file that is used to assess the data with respect to the reference genome.
The output is represented as characters that indicate the relation between the aligned and the reference sequence.
The meaning of the characters are:

  - . :base match on the forward strand

  - , :base match on the reverse strand

  - \</\> :reference skip

  - AGTCN :each one of these letters indicates a base that did not match the reference on the forward strand.

  - Agtcn : each one of these letters indicates a base that did not match the reference on the reverse strand.

  - \+ [0-9]+[AGTCNagtcn] : Denotes (an) insertion(s) of a number of the indicated bases.

  - \-[0-9]+[AGTCNagtcn] : Denotes (an) deletion(s) of a number of the indicated bases.

  - ^ : Start of a read segment. A following character indicates the
    mapping quality based on phred33 score.

  - $ : End of a read segment.

  - \* : Placeholder for a deleted base in a multiple basepair
    deletion.

  - `quickcheck` Checks if a .bam or .sam file is ok. If there is no output, the file is good. If and only if there are warnings, an output is generated. If an output is wanted anyways, use the command `samtools quickcheck –v [input.bam] &&echo ‘All ok’ || echo ‘File failed check’`

Create a .bam file using the command

```{bash}
samtools view –b ${path_align_out}${filename_trimmed::-6}'.sam' > ${path_align_out} ${filename_trimmed::-6}'.bam'
```

Check if everything is ok with the .bam file using

```{bash}

samtools quickcheck ${path_align_out}${filename_trimmed::-6}'.bam'
```

- This checks if the file appears to be intact by checking the header is valid, there are sequences in the beginning of the file and that there is a valid End-Of_File command at the end.
- It thus check only the beginning and the end of the file and therefore any errors in the middle of the file are not noted.
- But this makes this command really fast.
- If no output is generated, the file is good.

If desired, more information can be obtained using :

```{bash}
samtools flagstat ${path_align_out}${filename_trimmed::-6}'.bam'
```

```{bash}
samtools stats ${path_align_out}${filename_trimmed::-6}'.bam'
```

Especially the latter can be a bit overwhelming with data, but this gives a thorough description of the quality of the bam file.
For more information see [this documentation](http://www.htslib.org/doc/1.6/samtools.html).

For many downstream tools, the .bam file needs to be sorted.
This can be done using SAMtools, but this might give problems.
A faster and more reliable method is using the software sambamba using the command

```{bash}

sambamba-0.7.1-linux-static sort –m 500MB ${path_align_out}${filename_trimmed::-6}'.bam'
```

(where `–m` allows for specifying the memory usage which is 500MB in this example).
This creates a file with the extension .sorted.bam, which is the sorted version of the original bam file.
Also an index is created with the extension .bam.bai.
If this latter file is not created, it can be made using the command

```{bash}
sambamba-0.7.1-linux-static index  ${path_align_out}${filename_trimmed::-6}'.bam'
```

Now the reads are aligned to the reference genome and sorted and indexed.
Further analysis is done in windows, meaning that the sorted .bam files needs to be moved to the shared folder.

```{bash}
mv ${pathdata} ${path_sf}
```

Next, the data analysis is performed using custom made codes in Matlab in Windows.

### 5. Determining transposon insertions: Matlab (Code from Benoit [Michel et. al. 2017])

Before the data can be used as an input for the Matlab code provided by the Kornmann lab, it needs to be copied from the shared folder to the data folder using the command:

```{bash}
mv "${path_sharedfolder}/"* ${path_align_out}
```

The Matlab code is provided by Benoit (see the [website](https://sites.google.com/site/satayusers/complete-protocol/bioinformatics-analysis/matlab-script)) and is based on the [paper by Michel et. al.](<https://elifesciences.org/articles/23570>).
Running the code requires the user to select a .bam  or .sorted.bam file (or .ordered.bam which is similar to the .sorted.bam).
If the .bam file is chosen or there is no .bam.bai (bam index-)file present in the same folder, the script will automatically generate the .sorted.bam and a .bam.bai file.
In the same folder as the bam file the Matlab variables ‘yeastGFF.mat’ and ‘names.mat’ should be present (which can be found on the [website cited above](https://sites.google.com/site/satayusers/complete-protocol/bioinformatics-analysis/matlab-script)).
The script will generate a number of files (some of them are explained below):

1. .sorted.bam (if not present already)

2. .bam.bai (if not present already)

3. .sorted.bam.linearindex

4. .sorted.bam.mat (used as a backup of the matlab script results)

5. .sorted.bam_pergene.txt (contains information about transposons and reads for individual genes)

6. .sorted.bam.bed (contains information about the location and the number of reads per transposon insertion)

7. .sorted.bam.wig (contains information about the location and the number of reads per transposon insertion)

The line numbers below correspond to the original, unaltered code.

[line1-13] After loading the .BAM file, the ‘baminfo’ command is used
to collect the properties for the sequencing data. These include (among
others) [<https://nl.mathworks.com/help/bioinfo/ref/baminfo.html>]:

- `SequenceDictionary`: Includes the number of basepairs per
    chromosome.

- `ScannedDictionary`: Which chromosomes are read (typically 16 and
    the mitochondrial chromosome).

- `ScannedDictionaryCount`: Number of reads aligned to each reference
    sequence.

[line22-79] Then, a for-loop over all the chromosomes starts (17 in
total, 16 chromosomes and a mitochondrial chromosome). The for-loop
starts with a BioMap command which gets the columns of the SAM-file. The
size of the columns corresponds with the number of reads aligned to each
reference sequence (see also the ‘baminfo’ field `ScannedDictionaryCount`). The collected information is:

- `SequenceDictionary`: Chromosome number where the reads are
    collected for (given in roman numerals or ‘Mito’ for mitochondrial).
    (QNAME)

- `Reference`: Chromosome number that is used as reference sequence.
    (RNAME)

- `Signature`: CIGAR string. (CIGAR)

- `Start`: Start position of the first matched basepair given in terms
    of position number of the reference sequence. (POS)?

- `MappingQuality`: Value indicating the quality of the mapping. When
    60, the mapping has the smallest chance to be wrong. (MAPQ)

- `Flag`: Flag of the read. (FLAG)

- `MatePosition`: (PNEXT)?

- `Quality`: Quality score given in FASTQ format. Each ASCII symbol
    represents an error probability for a base pair in a read. See
    [<https://drive5.com/usearch/manual/quality_score.html>] for a
    conversion table. (QUAL)

- `Sequence`: Nucleotide sequence of the read. Length should math the
    length of the corresponding ‘Quality’ score. (SEQ)

- `Header`: Associated header for each read sequence.

- `Nseqs`: Integer indicating the number of read sequences for the
    current chromosome.

- `Name`: empty

(Note: Similar information can be obtained using the ‘bamread’ command
(although his is slower than ‘BioMap’), which gives a structure element
with fields for each piece of information. This can be accessed using:
`bb = bamread(file,infobam.SequenceDictionary(kk).SequenceName,\[1
infobam.SequenceDictionary(kk).SequenceLength\]))`
`bb(x).’FIELD’ %where x is a row (i.e. a specific read) and FIELD
is the string of the field.`)

After extracting the information from the SAM-file (using the ‘BioMap’
command), the starting site is defined for each read. This is depended
on the orientation of the read sequence. If this is normal orientation
it has flag=0, if it is in reverse orientation it has flag=16. If the
read sequence is in reverse orientation, the length of the read sequence
(‘readlength’ variable) needs to be added to the starting site (‘start’
variable). The corrected starting sites of all reads are saved in a new
variable (‘start2’). Note that this changes the order of which the reads
are stored. To correct this, the variables ‘start2’ and ‘flag2’ are
sorted in ascending order.

Now, all the reads in the current chromosome are processed. Data is
stored in the ‘’tncoordinates’ variable. This consists of three numbers;
the chromosome number (‘kk’), start position on the chromosome
(‘start2’) and the flag (‘flag2’). All reads that have the same
starting position and the same flag (i.e. the same reading orientation)
are stored as a single row in the ‘tncoordinates’ variable (for this the
average starting position is taken). This results in an array where each
row indicates a new starting position and the reading orientation. The
number of measurements that were averaged for a read is stored in the
variable ‘readnumb’. This is important later in the program for
determining the transposons.

This is repeated for each chromosome due to the initial for-loop. The
‘tnnumber’ variable stores the number of unique starting positions and
flags for each chromosome (this does not seem to be used anywhere else
in the program).

[line94-120] After getting the needed information from the SAM-file,
the data needs to be compared with the literature. For this yeastGFF.mat
is used (provided by Benoit et. al.) that loads the variable ‘gff’. This
includes all genes (from SGD) and the essential genes (from YeastMine).
(Note that a similar list can be downloaded from the SGD website as a
text file). The file is formatted as a matrix with in each row a DNA
element (e.g. genes) and each column represent a different piece of
information about that element. The used columns are:

1. Chromosome number (represented as roman numerals)

2. Data source (either SGD, YeastMine or landmark. Represented as a
    string)

3. Type of the DNA element, e.g. gene. The first element of a
    chromosome is always the ‘omosome’, which is the entire chromosome
    (Represented as a string)

4. Start coordinates (in terms of base pairs. Represented as an
    integer)

5. End coordinates (in terms of base pairs. Represented as an integer)

6. A score value. Always a ‘.’ Represented as a string indicating a
    dummy value.

7. Reading direction (+ for forward reading (5’-3’), - for reverse
    reading (3’-5’), ‘.’ If reading direction is undetermined.
    Represented as a string)

8. Always a ‘.’ Except when the element is a Coding DNA Sequence (CDS),
    when this column become a ‘0’. A CDS always follows a gene in the
    list and the value indicates how many basepairs should be removed
    from the beginning of this feature in order to reach the first codon
    in the next base (Represented as a string)

9. Other information and notes (Represented as a string)

From the ‘gff’ variable, all the genes are searched and stored in the
variable ‘features.genes’ (as a struct element). The same thing is done
for the essential genes by searching for genes from the ‘YeastMine’
library and these are stored in ‘features.essential’ (as a struct
element). This results in three variables:

- `features`: struct element that includes the fields ‘genes’ and
    ‘essential’ that include numbers representing in which rows of the
    ‘gff’ variable the (essential) gene can be found (note that the
    essential genes are indicated by ‘ORF’ from ’Yeastmine’ in the ‘gff’
    variable).

- `genes`: struct element storing the start and end coordinates (in
    basepairs) and the chromosome number where the gene is found.

- `essential`: struct element. Same as ‘genes’, but then for essential
    genes as found by the ‘YeastMine’ database.

This can be extended with other features (e.g. rRNA, see commented out
sections in the code).

[line124-160] Next all the data is stored as if all the chromosomes
are put next to each other. In the `tncoordinates` variable, for each
chromosome the counting of the basepairs starts at 1. The goal of this
section is to continue counting such that the first basepair number of a
chromosome continues from the last basepair number of the previous
chromosome (i.e. the second chromosome is put after the first, the third
chromosome is put after the second etc., to create one very long
chromosome spanning the entire DNA). The first chromosome is skipped
(i.e. the for-loop starts at 2) because these basepairs does not need to
be added to a previous chromosome. This is repeated for the start and
end coordinates of the (essential) genes.

[line162-200] Now the number of transposons is determined which is
done by looking at the number of reads per gene. First, all the reads
are found that have a start position between the start and end position
of the known genes. The indices of those reads are stored in the
variable ‘xx’. In the first for-loop of the program (see lines 22-79)
the reads (or measurements) that had the same starting position and flag
where averaged and represented as a single read. To get the total number
of reads per gene the number of measurements that were used for
averaging the reads corresponding to the indices in ‘xx’ are summed (the
value stored in the variable ‘readnumb’). This is repeated for all genes
and the essential genes using a for-loop. The maximum value is
subtracted as a feature to suppress noise or unmeaningful data (see a
more detailed explanation the discussion by Galih in the forum of Benoit [https://groups.google.com/forum/#!category-topic/satayusers/bioinformatics/uaTpKsmgU6Q]).

[line226-227] Next all variables in the Matlab workspace are saved
using the same name as the .bam file, but now with the .mat extension.
The program so far does not need to be ran all over again but loading
the .mat file loads all the variables.

Next a number of files are generated (.bed, .txt and .wig).

[line238-256] A .bed file is generated that can be used for
visualization of the read counts per insertion site. This contains
the information stored in the ‘tncoordinates’ variable. This includes
the chromosome number and the start position of the reads. The end
position of the reads is taken as the start position +1 (The end
position is chosen like this just to visualize the transposon insertion
site). The third column is just a dummy variable and can be ignored. As
the reads were averaged if multiple reads shared the same location on
the genome, the total number of reads is taken from the ‘readnumb’
variable and is stored in the fourth column of the file using the
equation 100+readnumb(i)\*20 (e.g. a value of 4 in `readnumb` is stored as 180 in the .bed file).

In general a .bed file can contain 12 columns, but only the first three
columns are obligatory. These are the chromosome number, start position
and end position (in terms of basepairs), respectively. More information
can be added as is described in the links below. If a column is filled,
then all the previous columns need to be filled as well. If this
information is not present or wanted, the columns can be filled with a
dummy character (typically a dot is used) [<https://bedtools.readthedocs.io/en/latest/content/general-usage.html>] [<https://learn.gencore.bio.nyu.edu/ngs-file-formats/bed-format/>].

[line238-256] Next a text file is generated for storing information
about the transposon counts per gene. This is therefore a summation of
all the transposons that have an insertion site within the gene. (To
check a value in this file, look up the location of a gene present in
this file. Next look how many transposon are located within the range
spanned by the gene using the .bed file). To create this the names.mat
file is needed to create a list of gene names present in the first
column. The transposon count is taken from the `tnpergene` variable and
is stored in the second column of the file. The third is the number of
reads per gene which is taken from the `readpergene` variable (which is
calculated by `readnumb-max(readnumb)` where the `readnumb` variable is
used for keeping track of the number of reads that were used to average
the reads).

[line260-299] Creating a .wig file. This indicates the transposon
insertion sites (in terms of basepairs, starting counting from 1 for
each new chromosome). The file consists of two columns. The first column
represent the insertion site for each transposons and the second column
is the number of reads in total at that location. The
information is similar to that found in the .bed file, but here the
read count is the actual count (and thus not used the equation
100+transposon_count*20 as is done in the .bed file).

## Bibliography

Chen, P., Wang, D., Chen, H., Zhou, Z., & He, X. (2016). The nonessentiality of essential genes in yeast provides therapeutic insights into a human disease. Genome research, 26(10), 1355-1362.

Del Fabbro, C., Scalabrin, S., Morgante, M., & Giorgi, F. M. (2013). An extensive evaluation of read trimming effects on Illumina NGS data analysis. PloS one, 8(12).

Delhomme, N., Mähler, N., Schiffthaler, B., Sundell, D., Mannepperuma, C., & Hvidsten, T. R. (2014). Guidelines for RNA-Seq data analysis. Epigenesys protocol, 67, 1-24.

MacManes, M. D. (2014). On the optimal trimming of high-throughput mRNA sequence data. Frontiers in genetics, 5, 13.

Michel, A. H., Hatakeyama, R., Kimmig, P., Arter, M., Peter, M., Matos, J., ... & Kornmann, B. (2017). Functional mapping of yeast genomes by saturated transposition. Elife, 6, e23570.

Pfeifer, S. P. (2017). From next-generation resequencing reads to a high-quality variant data set. Heredity, 118(2), 111-124.

Segal, E. S., Gritsenko, V., Levitan, A., Yadav, B., Dror, N., Steenwyk, J. L., ... & Kunze, R. (2018). Gene essentiality analyzed by in vivo transposon mutagenesis and machine learning in a stable haploid isolate of Candida albicans. MBio, 9(5), e02048-18.

Usaj, M., Tan, Y., Wang, W., VanderSluis, B., Zou, A., Myers, C. L., ... & Boone, C. (2017). TheCellMap. org: A web-accessible database for visualizing and mining the global yeast genetic interaction network. G3: Genes, Genomes, Genetics, 7(5), 1539-1549

+++

> ***"I want to be a healer, and love all things that grow and are not barren"***
> - J.R.R. Tolkien
