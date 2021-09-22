import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np 
import pkg_resources


from transposonmapper.properties import chromosome_position,gene_aliases
from transposonmapper.processing import chromosome_name_wigfile

from transposonmapper.processing.read_sgdfeatures import sgd_features


from transposonmapper.importing import (
    load_default_files, load_sgd_tab
)


from transposonmapper.processing.dna_features_helpers import (build_dataframe, input_region, intergenic_regions, read_pergene_file, 
                                                              read_wig_file,gene_location,checking_features)
from transposonmapper.plotting.dna_features_plot import dna_features_plot

def dna_features(region, wig_file, pergene_insertions_file, variable="reads", plotting=True, savefigure=False, verbose=True):
    """This scripts takes a user defined genomic region (i.e. chromosome number, region or gene) and creates a dataframe including information about all genomic features in the chromosome (i.e. genes, nc-DNA etc.).
    This can be used to determine the number of reads outside the genes to use this for normalization of the number of reads in the genes.
    Output is a dataframe including major information about all genomic features and optionally a barplot indicating the number of transposons per genomic region.
    A genomic region is here defined as a gene (separated as annotated essential and not essential), telomere, centromere, ars etc.
    This can be used for identifying neutral regions (i.e. genomic regions that, if inhibited, do not influence the fitness of the cells).
    This function can be used for normalizing the transposon insertions per gene using the neutral regions.
    
              
    
    Parameters
    ----------
    region : str
        - Region: e.g. chromosome number (either a normal number between 1 and 16 or in roman numerals between I and XVI), a list like ['V', 0, 14790] which creates a barplot between basepair 0 and 14790) or a genename.

    wig_file : str
        absolute path for the wig file location
    pergene_insertions_file : str 
        asbsoulte path for the _pergene_insertions.txt file location 
    variable : str, optional
        By default "reads". It could be "transposons"or "reads". This would be used for the plotting if True 
    plotting : bool, optional
        Whether or not producing a bar plot with the reads/insertions per genomic location in the region, by default True
    savefigure : bool, optional
        Whether or not saving the plot in the same folder as the datafiles, by default False
    verbose : bool, optional
        Determines how much textual feedback is given. When set to False, only warnings will be shown. By default True

    Returns
    -------
    dataframe
         Dataframe containing information about the selected chromosome. 

    
    """

    # If necessary, load default files
    gff_file, essentials_file, gene_information_file = load_default_files()
    sgd_features_file=load_sgd_tab()

    # Verify presence of files
    data_files = {
        "gff3": gff_file,
        "essentials": essentials_file,
        "gene_names": gene_information_file,
        "sgd_features": sgd_features_file
    }

    for filetype, file_path in data_files.items():
        assert file_path, f"{filetype} not found at {file_path}"


    variable = variable.lower()
    if plotting == True:
        create_plottitle = ''

# DETERMINE INPUTTED REGION

    roi_start,roi_end,region_type,chrom=input_region(region=region,verbose=verbose)

    

#READ WIG FILE FOR GETTING LOCATIONS OF ALL TN INSERTIONS

    insrt_in_chrom_list,reads_in_chrom_list=read_wig_file(wig_file=wig_file,chrom=chrom)


# READ PERGENE_INSERTIONS FILE FOR LOCATION OF ALL INSERTIONS PER EACH GENE.

    gene_position_dict=read_pergene_file(pergene_insertions_file=pergene_insertions_file,chrom=chrom)

# DETERMINE THE LOCATION GENOMIC FEATURES IN THE CURRENT CHROMOSOME AND STORE THIS IN A DICTIONARY

    dna_dict,start_chr,end_chr,len_chr,feature_orf_dict=gene_location(chrom,gene_position_dict,verbose)

## GET FEATURES FROM INTERGENIC REGIONS 

    dna_dict_new,genomicregions_list=intergenic_regions(chrom,start_chr,dna_dict)


    ### TEST IF ELEMENTS IN FEATURE_ORF_DICT FOR SELECTED CHROMOSOME ARE THE SAME AS THE GENES IN GENE_POSITION_DICT BY CREATING THE DICTIONARY FEATURE_POSITION_DICT CONTAINING ALL THE GENES IN FEATURE_ORF_DICT WITH THEIR CORRESPONDING POSITION IN THE CHROMOSOME
    checking_features(feature_orf_dict,chrom,gene_position_dict,verbose)

    dna_df2=build_dataframe(dna_dict_new,start_chr,end_chr,insrt_in_chrom_list,reads_in_chrom_list,genomicregions_list,chrom)

    #PRINT INFORMATION FOR THE SELECTED GENE
    if region_type == 'Gene':
        for region_info in dna_df2.itertuples():
            if region_info.Feature_name == region.upper() or region_info.Standard_name == region.upper():
                print(region_info)

    
    # CREATE BAR PLOT 
    dna_features_plot(chrom, dna_df2,roi_start,roi_end,len_chr,plotting,variable)

    if savefigure == True:
        file_dirname=pkg_resources.resource_filename("transposonmapper", "data_files/")
        if variable == 'reads':
            saving_name = os.path.join(file_dirname,'GenomicFeaturesReads_Barplot_Chrom'+chrom+'_NonNormalized')
        else:
            saving_name = os.path.join(file_dirname,'GenomicFeaturesInsertions_Barplot_Chrom'+chrom+'_NonNormalized')
        plt.savefig(saving_name, orientation='landscape', dpi=200)
        plt.close()

    return(dna_df2)






