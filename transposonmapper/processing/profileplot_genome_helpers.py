from transposonmapper.processing.chromosome_names_in_files import chromosome_name_bedfile
from transposonmapper.properties.get_chromosome_position import chromosome_position

import numpy as np 

def summed_chr(chr_length_dict):
    """Create a dictionary where each value is the cumulative sum of all bp in each chromosomes

    Parameters
    ----------
    chr_length_dict : dict
        A dictionary describing the length of each chromosome. 

    Returns
    -------
    dict
        A dictionary where each value corresponds to the cumulative sum of the previous chromosomes lengths. 
    """
    
    chrom_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']
    summed_chr_length_dict = {}
    summed_chr_length = 0
    for c in chrom_list:
        summed_chr_length_dict[c] = summed_chr_length
        summed_chr_length += chr_length_dict.get(c)    
     
    return summed_chr_length_dict


def length_genome(chr_length_dict):
    
    """Output the length of the genome in bp 

    Parameters
    ----------

    chr_length_dict : dict
        A dictionary describing the length of each chromosome. 

    Returns
    -------
    int
        The length of the genome
    """
    
    chrom_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']

    l_genome = 0
    for chrom in chrom_list:
        l_genome += int(chr_length_dict.get(chrom))
   
    
    return l_genome



def middle_chrom_pos(chr_length_dict):
    """Defines the middle poit of each chromosome

    Parameters
    ----------
    chr_length_dict : dict
        A dictionary describing the length of each chromosome. 

    Returns
    -------
    list
        A list describing for each chromosome the middle point. 
    """
    
    summed_chr_length_dict=summed_chr(chr_length_dict)
    
    l_genome=length_genome(chr_length_dict)
    
    
    middle_chr_position = []
    c1 = summed_chr_length_dict.get('I')
    for c in summed_chr_length_dict:
        if not c == 'I':
            c2 = summed_chr_length_dict.get(c)
            middle_chr_position.append(c1 + (c2 - c1)/2)
            c1 = c2
            
    c2 = l_genome
    middle_chr_position.append(c1 + (c2 - c1)/2)
    
    return middle_chr_position



def counts_genome(variable,bed_file,gff_file):
    """Counts of reads or the transposons per chromosomes

    Parameters
    ----------
    variable : str
        "transposons" or "reads"
    bed_file : str
        absolute path of the location of the bedfile
    gff_file : str
        absolute path of the location of the gff file 

    Returns
    -------
    numpy.ndarray
        An array of the length of the genome with the counts of each variable per location in the genome. 
    """
    
    with open(bed_file) as f:
        lines = f.readlines()
    
    chrom_names_dict, chrom_start_index_dict, chrom_end_index_dict= chromosome_name_bedfile(bed_file)
    chr_length_dict, chr_start_pos_dict, chr_end_pos_dict = chromosome_position(gff_file)
    
    summed_chr_length_dict=summed_chr(chr_length_dict)
    
    l_genome=length_genome(chr_length_dict)

    allcounts_list = np.zeros(l_genome)
    if variable == "transposons":
        for line in lines[chrom_start_index_dict.get("I"):chrom_end_index_dict.get("XVI")+1]:
            line = line.strip('\n').split()
            chrom_name = [k for k,v in chrom_names_dict.items() if v == line[0].replace("chr",'')][0]
            allcounts_list[summed_chr_length_dict.get(chrom_name) + int(line[1])-1] += 1
    elif variable == "reads":
        for line in lines[chrom_start_index_dict.get("I"):chrom_end_index_dict.get("XVI")+1]:
            line = line.strip('\n').split()
            chrom_name = [k for k,v in chrom_names_dict.items() if v == line[0].replace("chr",'')][0]
            allcounts_list[summed_chr_length_dict.get(chrom_name) + int(line[1])-1] += (int(line[4])-100)/20
    return allcounts_list

def binned_list(allcounts_list,bar_width):
    """A binned list for a histogram of the counts 

    Parameters
    ----------
    allcounts_list : numpy.ndarray
        Output of the counts_genome function
    bar_width : float 
        It could be a function of the length of the genome e.g. bar_width=l_genome/1000

    Returns
    -------
    list
        Binned list 
    """
    
    allcounts_binnedlist = []
    val_counter = 0
    sum_values = 0
    for n in range(len(allcounts_list)):
        if int(val_counter % bar_width) != 0:
            sum_values += allcounts_list[n]
        elif int(val_counter % bar_width) == 0:
            allcounts_binnedlist.append(sum_values)
            sum_values = 0
        val_counter += 1
    allcounts_binnedlist.append(sum_values)
    return allcounts_binnedlist