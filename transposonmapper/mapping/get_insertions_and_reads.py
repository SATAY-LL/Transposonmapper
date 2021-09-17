import numpy as np

def get_insertions_and_reads(coordinates, tn_coordinates, readnumb_array):
    """This function computes the total number of transposons per gene , the number of reads per gene and
    the distribution  of transposons along the gene.

    Parameters
    ----------
    coordinates : dict 
        This is the output of the function add_chromosome_length(coordinates, chr_lengths_cumsum, ref_tid_roman)
    tn_coordinates : numpy.array
        This is the output of the function add_chromosome_length_inserts(coordinates, ref_names, chr_lengths)
    readnumb_array : numpy.array
        This is the 1st output of the function get_reads(bam)

    Returns
    -------
     dict 
        A dict which every key corresponds with each gene and each value with the total number of transposons found in that gene
    
     dict
        A dict which every key corresponds with each gene and each value with the total number of reads for all the transposons found in that gene

     dict 
        A dict which every key corresponds with each gene and each value with a  list of 4 elements:
            - the chromosome number
            - gene start position
            - gene end position
            - distribution of reads per transposon found inside the gene 

    """

    tn_per_gene = {}
    reads_per_gene = {}
    tn_coordinates_per_gene = {}

    for gene in coordinates:
        xx = np.where(np.logical_and(tn_coordinates[:,1] >= coordinates.get(gene)[1], tn_coordinates[:,1] <= coordinates.get(gene)[2])) #get all insertions within range of current gene
        tn_per_gene[gene] = np.size(xx)
        reads_per_gene[gene] = sum(readnumb_array[xx]) - max(readnumb_array[xx], default=0) #REMOVE LARGEST VALUE TO REDUCE NOISE

        if np.size(xx) > 0:
            tn_coordinates_per_gene[gene] = [coordinates.get(gene)[0], coordinates.get(gene)[1], coordinates.get(gene)[2], list(tn_coordinates[xx[0][0]:xx[0][-1]+1, 1]), list(readnumb_array[xx])]
        else:
            tn_coordinates_per_gene[gene] = [coordinates.get(gene)[0], coordinates.get(gene)[1], coordinates.get(gene)[2], [], []]

    return tn_per_gene, reads_per_gene, tn_coordinates_per_gene