import os
import numpy as np
import re 

from transposonmapper.importing import load_default_files
from transposonmapper.processing import list_known_essentials

def read_pergene_file(pergenefile):
    """It reads the content of the pergene file , one of the outputs of Transposonmapper 

    Parameters
    ----------
    pergenefile : str
        absolute path to the pergene.txt file , one of the outputs of the transposonmapper module

    Returns
    -------
    list
        Gene names list
    list
        Insertion list
    list 
        Reads list 
    """

    assert os.path.isfile(pergenefile), 'File not found at: %s' % pergenefile

    with open(pergenefile) as f:
        lines = f.readlines()[1:] #skip header

    genenames_list = [np.nan]*len(lines)
    tnpergene_list = [np.nan]*len(lines)
    readpergene_list = [np.nan]*len(lines) 

    line_counter = 0
    for line in lines:
        line_split = re.split(' |\t', line.strip('\n'))
        l = [x for x in line_split if x]

        if len(l) == 3:
            genenames_list[line_counter] = l[0]
            tnpergene_list[line_counter] = int(l[1])
            readpergene_list[line_counter] = int(l[2])

            line_counter += 1
    return genenames_list,tnpergene_list,readpergene_list,lines


def reads_per_insertion(tnpergene_list,readpergene_list,lines):
    """It computes the reads per insertion following the formula:
    reads/(insertions-1) if the number of insertions is higher than 5, 
    if not then the reads per insertion will be 0. 

    Parameters
    ----------
    tnpergene_list : list
        A list with all insertions
    readpergene_list : list 
        A list of the reads 
    lines : int
        Number of genes mapped to in the reference genome 

    Returns
    -------
    list
         A list containing all the reads per insertions per gene. 
    """

    readperinspergene_list = [np.nan]*len(lines)
    for i in range(len(tnpergene_list)):
        if not tnpergene_list[i] < 5:
            readperinspergene_list[i] = readpergene_list[i] / (tnpergene_list[i] -1)
        else:
            readperinspergene_list[i] = 0

    return readperinspergene_list
    
def essential_genes(genenames_list,lines):
    """It provides a list of essential genes 

    Parameters
    ----------
    genenames_list : list
        A list will al genes names that were mapped to the reference genome
    lines : int 
        Number of genes in total 

    Returns
    -------
    list 
        List of essential genes 
    """

    _,essential_genes_list,_=load_default_files()
    known_essential_gene_list = list_known_essentials(essential_genes_list)
    geneessentiality_list = [None]*len(lines)
    for i in range(len(genenames_list)):
        if genenames_list[i] in known_essential_gene_list:
            geneessentiality_list[i] = True
        else:
            geneessentiality_list[i] = False
        
    return geneessentiality_list