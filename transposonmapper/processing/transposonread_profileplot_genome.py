
import os
import numpy as np
import matplotlib.pyplot as plt


from transposonmapper.properties.get_chromosome_position import chromosome_position
from transposonmapper.properties.get_gene_position import  gene_position
from transposonmapper.processing.chromosome_names_in_files import chromosome_name_bedfile
from transposonmapper.processing.essential_genes_names import list_known_essentials

from transposonmapper.importing import load_default_files

from transposonmapper.plotting import profile_genome_plot

from transposonmapper.processing.profileplot_genome_helpers import (summed_chr,
length_genome,middle_chrom_pos,counts_genome,binned_list)


def profile_genome(bed_file=None, variable="transposons", bar_width=None, savefig=False,showfig=False):
    '''
    Created on Thu Mar 18 13:05:39 2021

    @author: gregoryvanbeek
    This function creates a bar plot along the entire genome.
    The height of each bar represents the number of transposons or reads at the genomic position indicated on the x-axis.
    The input is as follows:
        - bed file
        - variable ('transposons' or 'reads')
        - bar_width
        - savefig

    The bar_width determines how many basepairs are put in one bin. Little basepairs per bin may be slow. Too many basepairs in one bin and possible low transposon areas might be obscured.
    For this a list for essential genes is needed (used in 'list_known_essentials' function) and a .gff file is required (for the functions in 'chromosome_and_gene_positions.py') and a list for gene aliases (used in the function 'gene_aliases')
    '''




    # If necessary, load default files
    gff_file, essential_file, gene_name_file = load_default_files(
        gff_file=None, essentials_file=None, gene_names_file=None
    )

    # Verify presence of files
    data_files = {
        "gff3": gff_file,
        "essentials": essential_file,
        "gene_names": gene_name_file,
    }

    for filetype, file_path in data_files.items():
        assert file_path, f"{filetype} not found at {file_path}"


    chrom_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']
    
    chr_length_dict, chr_start_pos_dict, chr_end_pos_dict = chromosome_position(gff_file)
    
   
    summed_chr_length_dict=summed_chr(chr_length_dict)
    
       
    l_genome=length_genome(chr_length_dict)
    
    if bar_width == None:
        bar_width = l_genome/1000
    
    print('Genome length: ', l_genome)
    
       
    middle_chr_position=middle_chrom_pos(chr_length_dict)

    gene_pos_dict = gene_position(gff_file)
    
    genes_currentchrom_pos_list = [k for k, v in gene_pos_dict.items()]
    
    genes_essential_list = list_known_essentials(essential_file)


    allcounts_list=counts_genome(variable,bed_file,gff_file)

    allcounts_binnedlist=binned_list(allcounts_list,bar_width)


    if bar_width == (l_genome/1000):
        allinsertionsites_list = np.linspace(0,l_genome,int(l_genome/bar_width+1))
    else:
        allinsertionsites_list = np.linspace(0,l_genome,int(l_genome/bar_width+2))


    ##########Ploting##############
    
    profile_genome_plot(bar_width,l_genome,allinsertionsites_list,allcounts_binnedlist,summed_chr_length_dict,
                         middle_chr_position,chrom_list,variable,genes_currentchrom_pos_list,gene_pos_dict)
    

    # saving the plot 
    if savefig == True and variable == "transposons":
        savepath = os.path.splitext(bed_file)
        print('saving figure at %s' % savepath[0]+'_transposonplot_genome.png')
        plt.savefig(savepath[0]+'_transposonplot_genome.png', dpi=400)
        plt.close()
    elif savefig == True and variable == "reads":
        savepath = os.path.splitext(bed_file)
        print('saving figure at %s' % savepath[0]+'_readplot_genome.png')
        plt.savefig(savepath[0]+'_readplot_genome.png', dpi=400)
        plt.close()
    if showfig==True:
        plt.show()
        
    return allinsertionsites_list,allcounts_binnedlist



