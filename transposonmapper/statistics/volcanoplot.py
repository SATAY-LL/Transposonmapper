import os, sys

import matplotlib.pyplot as plt


from transposonmapper.statistics.volcano_helpers import apply_stats,  info_from_datasets, make_datafile

def volcano(path_a, filelist_a, path_b, filelist_b, variable='read_per_gene', significance_threshold=0.01, normalize=True, trackgene_list=[], figure_title=""):
    """This script creates a volcanoplot to show the significance of fold change between two datasets.
    It is based on this website:
        - https://towardsdatascience.com/inferential-statistics-series-t-test-using-numpy-2718f8f9bf2f
        - https://www.statisticshowto.com/independent-samples-t-test/

    Code for showing gene name when hovering over datapoint is based on:
        - https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib

    T-test is measuring the number of standard deviations our measured mean is from the baseline mean, while taking into
    account that the standard deviation of the mean can change as we get more data
    This creates a volcano plot that shows the fold change between two libraries and the corresponding p-values.
    
    The fold change is determined by the mean of dataset b (experimental set) divided by the mean of dataset a (reference set).
    The datasets can be of different length.
    P-value is determined based on the student t-test (scipy.stats.ttest_ind).

    NOTE:
        The fold change is determined by the ratio between the reference and the experimental dataset.
        When one of the datasets is 0, this is false results for the fold change.
        To prevent this, the genes with 0 insertions are set to have 5 insertions, and the genes with 0 reads are set to have 25 reads.
        These values are determined in dicussion with the Kornmann lab.

    - Created on Tue Feb 16 14:06:48 2021
    - @author: gregoryvanbeek

 
    Parameters
    ----------
    path_a : str
        paths to location of the datafiles for library a 
    filelist_a : str
        list of the names of the datafiles for library a  located in path_a 
    path_b : str
        paths to location of the datafiles for library b
    filelist_b : str
        list of the names of the datafiles for  library b located in path_b 
    variable : str, optional
        tn_per_gene, read_per_gene or Nreadsperinsrt , by default 'read_per_gene'
    significance_threshold : float, optional
        Threshold value above which the fold change is regarded significant, only for plotting, by default 0.01
    normalize : bool, optional
        Whether to normalize variable. If set to True, each gene is normalized based on the total count in each dataset (i.e. each file in filelist_)
        , by default True
    trackgene_list : list, optional
        Enter a list of gene name(s) which will be highlighted in the plot (e.g. ['cdc42', 'nrp1']), by default []
    figure_title : str, optional
        The title of the figure if not empty, by default ""


    Returns
    -------
    dataframe

        A dataframe containing:
        
            - gene_names
            - fold change
            - t statistic
            - p value
            - whether p value is above threshold
    figure
        - volcanoplot with the log2 fold change between the two libraries and the -log10 p-value.

    """

### Making the whole datafile name 

    datafiles_list_a,datafiles_list_b=make_datafile(path_a,filelist_a,path_b,filelist_b)


### Extract information from datasets

    variable_a_array,variable_b_array,volcano_df,tnread_gene_a,_=info_from_datasets(datafiles_list_a,datafiles_list_b,variable,normalize)

### APPLY stats.ttest_ind(A,B)
    volcano_df=apply_stats(variable_a_array,variable_b_array,significance_threshold,volcano_df)

   


### Volcanoplot
    print('Plotting: %s' % variable)

    fig = plt.figure(figsize=(19.0,9.0))#(27.0,3))
    grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.0)
    ax = plt.subplot(grid[0,0])

    colors = {False:'black', True:'red'} # based on p-value significance 
    sc = ax.scatter(x=volcano_df['fold_change'], y=volcano_df['p_value'], alpha=0.4, marker='.', c=volcano_df['significance'].apply(lambda x:colors[x]))
    ax.grid(True, which='major', axis='both', alpha=0.4)
    ax.set_xlabel('Log2 FC')
    ax.set_ylabel('-1*Log10 p-value')
    if not figure_title == "":
        ax.set_title(variable + " - " + figure_title)
    else:
        ax.set_title(variable)
    ax.scatter(x=[],y=[],marker='.',color='black', label='p-value > {}'.format(significance_threshold)) #set empty scatterplot for legend
    ax.scatter(x=[],y=[],marker='.',color='red', label='p-value < {}'.format(significance_threshold)) #set empty scatterplot for legend
    ax.legend()
    if not trackgene_list == []:
        genenames_array = volcano_df['gene_names'].to_numpy()
        for trackgene in trackgene_list:
            trackgene = trackgene.upper()
            if trackgene in genenames_array:
                trackgene_index = tnread_gene_a.loc[tnread_gene_a['gene_names'] == trackgene].index[0]
                trackgene_annot = ax.annotate(volcano_df.iloc[trackgene_index,:]['gene_names'], (volcano_df.iloc[trackgene_index,:]['fold_change'], volcano_df.iloc[trackgene_index,:]['p_value']),
                            size=10, c='green', bbox=dict(boxstyle="round", fc="w"))
                trackgene_annot.get_bbox_patch().set_alpha(0.6)
            else:
                print('WARNING: %s not found' % trackgene)
        


    names = volcano_df['gene_names'].to_numpy()
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


    
    def update_annot(ind):
    
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        # text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
        #                         " ".join([names[n] for n in ind["ind"]]))
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        # annot.get_bbox_patch().set_alpha(0.4)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
                    
    fig.canvas.mpl_connect("motion_notify_event", hover)


## return function
    return(volcano_df)


