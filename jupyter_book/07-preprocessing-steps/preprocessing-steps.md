# Preprocessing steps

Before inputting the data into the satay pipeline, it is necessary to preprocess the data that comes from the sequencing company. 

The pipeline does not process each digestion separately and therefore any pre-processing and trimming of the restriction sites should be done **prior** to running the pipeline.

## What we do if the sequencing data is paired end: 

If the data is paired end, only one of the pairs will map to the transposon insertion site (the end that has been sequenced from the sequencing primer), while the other end will map back to a location arbitrarily far upstream or downstream of the insertion site (depends on where the restriction site is).

**Preprocessing steps prior to use the satay pipeline:**

- Convert the data to single end by:
    - Extracting the forward reads, which are the reads that contain the sequencing primer, as it is (harsh filtering) or allowing some mismatches in the sequencing primer, due to likely sequencing errors (gentle filtering). 
    - We use a bash script for each type of filtering, if you would like to use it , please contact us by writing [here](mailto:L.M.InigoDeLaCruz@tudelft.nl).
- Remove the sequence downstream the first restriction site for NiaIII and DpnII to avoid having chimeras sequences in our data, that have poor alignment.
    - Discard reads bellow 50bp after trimming of the restriction site to ensure a decent confidence alignment score for that read. 
    - We use a bash script for this, if you would like to use it , please contact us by writing [here](mailto:L.M.InigoDeLaCruz@tudelft.nl).
    - Technical explanation regarding this, thanks to [Agnes Michel from the Kornmann Lab](https://www.kornmann.group/people/agn%C3%A8s) : 

    *What happens is that during the ligation of the NlaIII or DpnII digests, more than one molecule can ligate together. The conditions are set to favor intramolecular ligation but I have seen that it is not always the case. At the beginning of setting up SATAY, we were identifying reads that were chimeric between 2 genome loci that had nothing to do with each other, even though we were sequencing only 75bp. In our case, it was usually because the first restriction site after the insertion was very close to the insertion point itself (less than 75bp), and the resulting digestion product was too small to self-religate. Instead, another random molecule of digested gDNA would ligate with it, creating a circular chimeric molecule. Because the restriction site was less than 75bp of the insertion point, the sequencing read was a chimer between the genuine transposon insertion site and whatever gDNA molecule had co-ligated. By barcoding the NlaIII and DpnII sub libraries and trimming the reads containing a restriction site (NlaIII for the NlaIII sublibrary, DpnII for the DpnII sublibrary), before aligning it, you can solve the problem. The important thing to visualize is that the transposon is itself digested. So one end of the digested product is the first NlaIII or DpnII site after the insertion point, but the other end is the transoson itself. So, if this molecule self ligate, then the sequencing reads from both ends will map to the transposon-genome junction. If intermolecualr ligation has happened, then the sequencing read that correspond to the NlaIII or DpnII side of the transposon will be the sequence of whatever digested piece of gDNA has co-ligated with the genuine insertion locus.*