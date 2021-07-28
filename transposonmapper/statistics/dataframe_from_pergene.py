
import os, sys
import numpy as np
import pandas as pd


from transposonmapper.processing import list_known_essentials
from transposonmapper.importing import load_default_files

from transposonmapper.statistics.dataframe_from_pergene_helpers import read_pergene_file

def dataframe_from_pergenefile(pergenefile, verbose=True):
    """This function creates a dataframe with the information from a pergene.txt file.
        
    
    The gene_essentiality is created based on the genes present in the Cerevisiae_EssentialGenes_List_1.txt and Cerevisiae_EssentialGenes_List_2.txt files
    The number of reads per insertion (Nreadsperinsrt) is determined by dividing the read_per_gene column by the tn_per_gene column.
    
    Author: Gregory van Beek

    Parameters
    ----------
    pergenefile : str
        absolute path to the pergene.txt file , one of the outputs of the transposonmapper module
    verbose : bool, optional
        [description], by default True
    Outputs
    -----------
    Output is a dataframe where each row is a single gene and with the following columns:
        - gene_names
        - gene_essentiality
        - tn_per_gene
        - read_per_gene
        - Nreadsperinsrt
    """

   
# read file
    genenames_list,tnpergene_list,readpergene_list,lines=read_pergene_file(pergenefile)

    

# determine number of reads per insertion per gene
    readperinspergene_list = [np.nan]*len(lines)
    for i in range(len(tnpergene_list)):
        if not tnpergene_list[i] == 0:
            readperinspergene_list[i] = readpergene_list[i] / tnpergene_list[i]
        else:
            readperinspergene_list[i] = 0

   

# determine essential genes
    _,essential_genes_list,_=load_default_files()
    known_essential_gene_list = list_known_essentials(essential_genes_list)

    geneessentiality_list = [None]*len(lines)
    for i in range(len(genenames_list)):
        if genenames_list[i] in known_essential_gene_list:
            geneessentiality_list[i] = True
        else:
            geneessentiality_list[i] = False


# create dataframe
    read_gene_dict = {"gene_names": genenames_list,
                      "gene_essentiality": geneessentiality_list,
                      "tn_per_gene": tnpergene_list,
                      "read_per_gene": readpergene_list,
                      "Nreadsperinsrt": readperinspergene_list}

    read_gene_df = pd.DataFrame(read_gene_dict, columns = [column_name for column_name in read_gene_dict])

    return(read_gene_df)


