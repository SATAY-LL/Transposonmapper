import warnings


def get_chromosome_names(bam):
    """ This functions translate the format of the chromosome names
    from the alignment file from the pysam module into numbers
    

    Parameters
    ----------
    bam : dict , It is the output of the function  pysam.AlignmentFile(bamfile, "rb")    

    Returns
    -------
    ref_tid : dict, where the values are the chromosome numbers per key in the bam file. 
    
    """

    # ref_tid = {str(name): int(bam.get_tid(name)) + 1 for name in bam.get_reference_name}

    ref_tid = {} # 'I' | 0, 'II' | 1, ...
    for i in range(bam.nreferences): #if bam.nreferences does not work, use range(17) #16 chromosomes and the mitochondrial chromosome
        ref_name = bam.get_reference_name(i)
        ref_tid[ref_name] = bam.get_tid(ref_name)

    return ref_tid


def get_sequence_length(bam):
    """ This function returns the length of each chromosome and a cumulative sum of them.
    
    Parameters
    ----------
    bam : dict, It is the output of the function  pysam.AlignmentFile(bamfile, "rb")          

    Returns
    -------
    chr_lengths : dict, A dictionary which very value is the length in basepairs
    of each chromosome in the alignment file. 
    chr_lengths_cumsum : dict , A dictionary which very value is the sum of the length in basepairs
    of the previous chromosomes in the alignment file. chr_lengths_cumsum{n}=cumulative sum (n-1 previous chromosomes
    length)

    """

    chr_lengths = {}  # 'I' | 230218, 'II' | 813184, ...
    chr_lengths_cumsum = {}  # 'I' | 0, 'II' | 230218, 'III' |  1043402, ...
    ref_summedlength = 0
    ref_tid = get_chromosome_names(bam)
    for key in ref_tid.keys():
        ref_length = bam.get_reference_length(key)
        chr_lengths[key] = bam.get_reference_length(key)
        chr_lengths_cumsum[key] = ref_summedlength
        ref_summedlength += ref_length

    return chr_lengths, chr_lengths_cumsum


def get_chromosome_reads(bam):
    """ This function returns statistics about mapped/unmapped reads per chromosome as they are stored in the index.
    It makes use of the method get_index_statistics() from the pysam module. 
    Parameters
    ----------
    bam : dict, It is the output of the function  pysam.AlignmentFile(bamfile, "rb")              

    Returns
    -------
    mapped_reads : dict[str, list]
        Syntax 'I' | [mapped, unmapped, total reads]

    """
    stats = bam.get_index_statistics()
    mapped_reads = {}
    for stat in stats:
        mapped_reads[stat[0]] = [stat[1], stat[2], stat[3]]
        if stat[2] != 0:
            warnings.warn("Unmapped reads found in chromosome " + stat[0])

    return mapped_reads
