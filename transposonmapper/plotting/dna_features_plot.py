        
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np 
        
def dna_features_plot(chrom, dna_df2,roi_start,roi_end,len_chr,plotting,variable):  
    """Plot function for the genomic features per chromosome 

    Parameters
    ----------
    chrom : str
        - Region: e.g. chromosome number (either a normal number between 1 and 16 or in roman numerals between I and XVI),
         a list like ['V', 0, 14790] which creates a barplot between basepair 0 and 14790) or a genename.
    dna_df2 : pandas.dataframe 
        Dataframe containing information about the selected chromosome
    roi_start : int
        The start of the chromosome
        roi_start,roi_end,region_type,chrom=input_region(region=region,verbose=verbose)
    roi_end : int
        The end of the chromosome
        roi_start,roi_end,region_type,chrom=input_region(region=region,verbose=verbose)
    len_chr : [type]
        Length of the  chromosome
        dna_dict,start_chr,end_chr,len_chr,feature_orf_dict=gene_location(chrom,gene_position_dict,verbose)
    plotting : optional
        default True
    variable : optional 
        default "reads"
    
    """ 


    if plotting == True:
        create_plottitle = chrom
        noncoding_color = "#002538"
        essential_color = "#10e372"
        nonessential_color = "#d9252e"
        codingdna_color = '#29a7e6'
        textcolor = "#000000"

        textsize = 14

        plt.figure(figsize=(19,9))
        grid = plt.GridSpec(20, 1, wspace=0.0, hspace=0.01)

        axc = plt.subplot(grid[19,0])

        axc.tick_params(labelsize=textsize)
        axc.set_yticklabels([])
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


        ax = plt.subplot(grid[0:19,0])
        

        ax.grid(linestyle='-', alpha=1.0)
        ax.tick_params(labelsize=textsize)

        ax.tick_params(axis='x', which='major', pad=30)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
        ax.xaxis.get_offset_text().set_fontsize(textsize)
        ax.set_xlabel("Basepair position on chromosome "+chrom, fontsize=textsize, color=textcolor, labelpad=10)
        ax.set_title(create_plottitle, fontsize=textsize, color=textcolor)


        feature_middle_pos_list = []
        sum_bp = 0
        for x in dna_df2['Nbasepairs']:
            feature_middle_pos_list.append(x/2 + sum_bp)
            sum_bp += x
        
        feature_width_list = list(dna_df2['Nbasepairs'])


        barcolor_list = []
        for feature in dna_df2['Feature_name']:
            if feature == 'noncoding':
                barcolor_list.append(noncoding_color)
            elif dna_df2.loc[dna_df2['Feature_name'] == feature]['Essentiality'].iloc[0] == False:
                barcolor_list.append(nonessential_color)
            elif dna_df2.loc[dna_df2['Feature_name'] == feature]['Essentiality'].iloc[0] == True:
                barcolor_list.append(essential_color)
            elif dna_df2.loc[dna_df2['Feature_name'] == feature]['Essentiality'].iloc[0] == None:
                barcolor_list.append(codingdna_color)

        

        legend_noncoding = mpatches.Patch(color=noncoding_color, label="Noncoding DNA")
        legend_essential = mpatches.Patch(color=essential_color, label="Annotated essential genes")
        legend_nonessential = mpatches.Patch(color=nonessential_color, label="Nonessential genes")
        legend_coding = mpatches.Patch(color=codingdna_color, label="Other genomic regions")
        leg = ax.legend(handles=[legend_noncoding, legend_essential, legend_nonessential, legend_coding]) #ADD

        for text in leg.get_texts():
            text.set_color(textcolor)
        
        if variable == "insertions":
            ax.bar(feature_middle_pos_list, list(dna_df2['Ninsertions']), feature_width_list, color=barcolor_list)
            ax.set_ylabel("Transposons per region", fontsize=textsize, color=textcolor)
        elif variable == "reads":
            ax.bar(feature_middle_pos_list, list(dna_df2['Nreads']), feature_width_list, color=barcolor_list)
            ax.set_ylabel("Reads per region", fontsize=textsize, color=textcolor)


        if roi_start != None and roi_end != None and roi_start < len_chr and roi_end < len_chr:
            ax.set_xlim(roi_start, roi_end)
        else:
            ax.set_xlim(0, len_chr)



        

        l = 0
        counter = 0
        for width in feature_width_list:
            if dna_df2.loc[counter][4] == True:
                axc.axvspan(l,l+width,facecolor=essential_color,alpha=0.3)
            elif dna_df2.loc[counter][4] == False and not dna_df2.loc[counter][0] == 'noncoding':
                axc.axvspan(l,l+width,facecolor=nonessential_color,alpha=0.3)
            elif dna_df2.loc[counter][4] == None and not dna_df2.loc[counter][0] == 'noncoding':
                axc.axvspan(l,l+width,facecolor=codingdna_color,alpha=0.5)
            l += width
            counter += 1
        if roi_start != None and roi_end != None and roi_start < len_chr and roi_end < len_chr:
            axc.set_xlim(roi_start, roi_end)
        else:
            axc.set_xlim(0, len_chr)
        
        