import numpy as np

def add_chromosome_length_inserts(coordinates, ref_names, chr_lengths):
    """ For each insertion location, add the length of all previous chromosomes

    Parameters
    ----------
    numpy.array
        Third output from get_reads(bam)
    list
    Output from the following : 
        ref_tid = get_chromosome_names(bam)

        ref_names = list(ref_tid.keys())

    dict
        First output from get_sequence_length(bam)
   

    Returns
    -------
    numpy.array
      For each insertion location, add the length of all previous chromosomes 
        
    """
    
    ll = 0
    for ii in range(1,len(ref_names)):
        ll += chr_lengths[ref_names[ii-1]]
        aa = np.where(coordinates[:,0] == ii + 1)
        coordinates[aa,1] = coordinates[aa,1] + ll

    return coordinates


def add_chromosome_length(coordinates, chr_lengths_cumsum, ref_tid_roman):
    
    """This function returns a dictionary that for every gene , there is the chromosome number
    information of where the gene belongs to , the coordinates for the start position, the end position
    and the direction of the gene. 

    Parameters
    ----------
    coordinates : dict 
        This dictionary is the 1st output from the function read_genes(gff_file, essentials_file, gene_names_file)
    chr_lengths_cumsum : dict
        This dictionary is the 2nd output from the function get_sequence_length(bam)
    ref_tid_roman : dict
        This dictionary is the output from 
        ref_tid_roman = {key: value for key, value in zip(ref_romannums, ref_tid)}, where
        ref_romannums = chromosomename_roman_to_arabic()[1] and 
        ref_tid = get_chromosome_names(bam)
        

    Returns
    -------
     dict
        A dictionary that for every gene , there is the chromosome number information of where the gene belongs to , the coordinates for the start position, the end position
    and the direction of the gene. 
    """  

    for key in coordinates:
        gene_chrom = ref_tid_roman.get(coordinates.get(key)[0])
        coordinates[key][1] = coordinates.get(key)[1] + chr_lengths_cumsum.get(gene_chrom)
        coordinates[key][2] = coordinates.get(key)[2] + chr_lengths_cumsum.get(gene_chrom)
    
    return coordinates

