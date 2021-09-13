import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np 

from transposonmapper.importing import load_default_files
from transposonmapper.processing import list_known_essentials

def profile_genome_plot(bar_width,l_genome,allinsertionsites_list,allcounts_binnedlist,summed_chr_length_dict,
                         middle_chr_position,chrom_list,variable,genes_currentchrom_pos_list,gene_pos_dict):
    """Plot function to show the whole insertion map throughout the genome 

    Parameters
    ----------
    bar_width : int
        The width for the histogram of the plot, by default None , which means internally the length of the genome over 1000 
    l_genome : int
        The length of the genome in bp
    allinsertionsites_list : list
        List of insertions sites 
    allcounts_binnedlist : list
        List of binned counts 
    summed_chr_length_dict : dict
        The cumulative sum of the length of every chromosome 
    middle_chr_position : dict
        Middle chromosome position per chromosome
    chrom_list : list
        A list of all the chromosomes
    variable : str
        It could be "transposons" or "reads"
    genes_currentchrom_pos_list : list
        List of genes per chromosome 
    gene_pos_dict : dict 
        Postion along the genome of every gene 
    """    

    _,essential_file,_=load_default_files()
    genes_essential_list=list_known_essentials(essential_file)


    plt.figure(figsize=(19.0,9.0))
    grid = plt.GridSpec(20, 1, wspace=0.0, hspace=0.0)

    textsize = 12
    textcolor = "#000000"
    barcolor= "#333333"
    chrom_color=(0.9,0.9,0.9,1.0)
    essential_face_color="#00F28E"
    non_essential_face_color="#F20064"
    alpha=0.8
    
    binsize = bar_width
    ax = plt.subplot(grid[0:19,0])
    ax.grid(False)
    ax.tick_params(axis='x', which='major', pad=30)
    
    
    
    axc = plt.subplot(grid[19,0])
    
    axc.set_xlim(0,l_genome)
    axc.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off

    axc.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left=False,        # ticks along the bottom edge are off
        right=False,       # ticks along the top edge are off
        labelleft=False)   # labels along the bottom edge are off
    
    ax.set_xlim(0,l_genome)
    
    # bar lines
    ax.bar(allinsertionsites_list,allcounts_binnedlist,width=binsize,color=barcolor)
   
    
    # chromosome lines
    for chrom in summed_chr_length_dict:
        ax.axvline(x = summed_chr_length_dict.get(chrom), linestyle='-', color=chrom_color)

    ax.set_xticks(middle_chr_position)
    ax.set_xticklabels(chrom_list, fontsize=textsize)
    
    # Axis labels
    if variable == "transposons":
        ax.set_ylabel('Transposon Count', fontsize=textsize, color=textcolor)
    elif variable == "reads":
        ax.set_ylabel('Read Count', fontsize=textsize, color=textcolor)

    # colored bars in the bottom 
    for gene in genes_currentchrom_pos_list:
        if not gene_pos_dict.get(gene)[0] == 'Mito':
            gene_start_pos = summed_chr_length_dict.get(gene_pos_dict.get(gene)[0]) + int(gene_pos_dict.get(gene)[1])
            gene_end_pos = summed_chr_length_dict.get(gene_pos_dict.get(gene)[0]) + int(gene_pos_dict.get(gene)[2])
            if gene in genes_essential_list:
                axc.axvspan(gene_start_pos,gene_end_pos,facecolor=essential_face_color,alpha=alpha)
            else:
                axc.axvspan(gene_start_pos,gene_end_pos,facecolor=non_essential_face_color,alpha=alpha)
    
