import matplotlib.pyplot as plt
import numpy as np 
import os 
from scipy import stats

from transposonmapper.statistics import dataframe_from_pergenefile

def make_datafile(path_a,filelist_a,path_b,filelist_b):
    """Assembly the datafile name to analyze 

    Parameters
    ----------
    path_a : str
        Path of the files corresponding to the reference library
    filelist_a : list of str 
        List of the filenames of the different replicates from the reference library.
        It has to have minimum two replicates per library, so the list has to contain
        a minimum of two files. 
    path_b : str 
        Path of the files corresponding to the experimental library
    filelist_b : list of str
        List of the filenames of the different replicates from the experimental library.
        It has to have minimum two replicates per library, so the list has to contain
        a minimum of two files. 


    Returns
    -------
    str
        Complete paths of the reference and the experimental libraries 
    """
    datafiles_list_a = []
    datafiles_list_b = []
    for files in filelist_a:
        datafile = os.path.join(path_a, files)
        assert os.path.isfile(datafile), 'File not found at: %s' % datafile
        datafiles_list_a.append(datafile)
    for files in filelist_b:
        datafile = os.path.join(path_b, files)
        assert os.path.isfile(datafile), 'File not found at: %s' % datafile
        datafiles_list_b.append(datafile)
    return datafiles_list_a,datafiles_list_b


def info_from_datasets(datafiles_list_a,datafiles_list_b,variable,normalize):
    """Read the information contain in the datafiles for the volcano plot 

    Parameters
    ----------
    datafiles_list_a : list of str 
        List of the absolute paths of all the replicates from the 
        reference library. 
    datafiles_list_b : list of str 
        List of the absolute paths of all the replicates from the 
        experimental  library. 
    variable : str
        Magnitude indicating based on what to make the volcano plot. 
        For example: tn_per_gene, read_per_gene or Nreadsperinsrt 

    normalize : bool 
        If True , If set to True, each gene is normalized based on 
        the total count in each dataset (i.e. each file in filelist_)
        

    Returns
    -------
    variable_a_array : numpy.array
    variable_b_array: numpy.array
    volcano_df: pandas.core.frame.DataFrame
    tnread_gene_a: pandas.core.frame.DataFrame
    tnread_gene_b: pandas.core.frame.DataFrame
    """

    tn_per_gene_zeroreplace = 5 #Add 5 insertions to every gene
    read_per_gene_zeroreplace = 25 #Add 25 reads to every gene
    # norm_a = 0
    # norm_b = 0
    for count, datafile_a in enumerate(datafiles_list_a):
        tnread_gene_a = dataframe_from_pergenefile(datafile_a, verbose=False)
        if normalize == True:
            if variable == 'tn_per_gene':
                norm_a = sum(tnread_gene_a.tn_per_gene)#*10**-4
            elif variable == 'read_per_gene':
                norm_a = sum(tnread_gene_a.read_per_gene)#*10**-7
            elif variable == 'Nreadsperinsrt':
                norm_a = sum(tnread_gene_a.Nreadsperinsrt)

        #ADD A CONSTANT TO ALL VALUES TO PREVENT A ZERO DIVISION WHEN DETERMINING THE FOLD CHANGE.
        tnread_gene_a.tn_per_gene = tnread_gene_a.tn_per_gene + tn_per_gene_zeroreplace
        tnread_gene_a.read_per_gene = tnread_gene_a.read_per_gene + read_per_gene_zeroreplace
        tnread_gene_a.Nreadsperinsrt = tnread_gene_a.Nreadsperinsrt + (read_per_gene_zeroreplace/tn_per_gene_zeroreplace)

        if count == 0:
            volcano_df = tnread_gene_a[['gene_names']] #initialize new dataframe with gene_names
            if normalize == True:
                variable_a_array = np.divide(tnread_gene_a[[variable]].to_numpy(), norm_a) #create numpy array to store normalized data
            else:
                variable_a_array = tnread_gene_a[[variable]].to_numpy() #create numpy array to store raw data
        else: 
            if normalize == True:
                variable_a_array = np.append(variable_a_array, np.divide(tnread_gene_a[[variable]].to_numpy(), norm_a), axis=1) #append normalized data
            else:
                variable_a_array = np.append(variable_a_array, tnread_gene_a[[variable]].to_numpy(), axis=1) #append raw data


    for count, datafile_b in enumerate(datafiles_list_b):
        tnread_gene_b = dataframe_from_pergenefile(datafile_b, verbose=False)
        if normalize == True:
            if variable == 'tn_per_gene':
                norm_b = sum(tnread_gene_b.tn_per_gene)#*10**-4
            elif variable == 'read_per_gene':
                norm_b = sum(tnread_gene_b.read_per_gene)#*10**-7
            elif variable == 'Nreadsperinsrt':
                norm_b = sum(tnread_gene_b.Nreadsperinsrt)

        #ADD A CONSTANT TO ALL VALUES TO PREVENT A ZERO DIVISION WHEN DETERMINING THE FOLD CHANGE.
        tnread_gene_b.tn_per_gene = tnread_gene_b.tn_per_gene + tn_per_gene_zeroreplace
        tnread_gene_b.read_per_gene = tnread_gene_b.read_per_gene + read_per_gene_zeroreplace
        tnread_gene_b.Nreadsperinsrt = tnread_gene_b.Nreadsperinsrt + (read_per_gene_zeroreplace/tn_per_gene_zeroreplace)

        if count == 0:
            if normalize == True:
                variable_b_array = np.divide(tnread_gene_b[[variable]].to_numpy(), norm_b)
            else:
                variable_b_array = tnread_gene_b[[variable]].to_numpy()
        else:
            if normalize == True:
                variable_b_array = np.append(variable_b_array, np.divide(tnread_gene_b[[variable]].to_numpy(), norm_b), axis=1)
            else:
                variable_b_array = np.append(variable_b_array, tnread_gene_b[[variable]].to_numpy(), axis=1)

    return variable_a_array,variable_b_array,volcano_df,tnread_gene_a,tnread_gene_b


def apply_stats(variable_a_array,variable_b_array,significance_threshold,volcano_df):
    """[summary]

    Parameters
    ----------
    variable_a_array : [type]
        [description]
    variable_b_array : [type]
        [description]
    significance_threshold : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    
    ttest_tval_list = [np.nan]*len(variable_a_array) #initialize list for storing t statistics
    ttest_pval_list = [np.nan]*len(variable_a_array) #initialize list for storing p-values
    signif_thres_list = [False]*len(variable_a_array) #initialize boolean list for indicating datapoints with p-value above threshold
    fc_list = [np.nan]*len(variable_a_array) #initialize list for storing fold changes

    for count,val  in enumerate(variable_a_array):

        ttest_val = stats.ttest_ind(variable_a_array[count], variable_b_array[count]) #T-test
        ttest_tval_list[count] = ttest_val[0]
        if not ttest_val[1] == 0: #prevent p=0 to be inputted in log
            ttest_pval_list[count] = -1*np.log10(ttest_val[1])
        else:
            ttest_pval_list[count] = 0
        if ttest_pval_list[count] > -1*np.log10(significance_threshold):
            signif_thres_list[count] = True

    #DETERMINE FOLD CHANGE PER GENE
        if np.mean(variable_b_array[count]) == 0 and np.mean(variable_a_array[count]) == 0:
            fc_list[count] = 0
        else:
            fc_list[count] = np.log2(np.mean(variable_a_array[count]) / np.mean(variable_b_array[count]))

    
    volcano_df['fold_change'] = fc_list
    volcano_df['t_statistic'] = ttest_tval_list
    volcano_df['p_value'] = ttest_pval_list
    volcano_df['significance'] = signif_thres_list

    return volcano_df
 
    

