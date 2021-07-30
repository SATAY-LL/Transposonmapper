import numpy 

from transposonmapper.statistics import make_datafile, info_from_datasets, apply_stats


def test_make_datafile():
    "checking outout variable type and format"
    path='transposonmapper/data_files/files4test/'
    file_a= ['WT_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'WT_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    file_b= ['dnrp1-1_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'dnrp1-1_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    
    datafile_a,datafile_b=make_datafile(path,file_a,path,file_b)
    
    assert isinstance(datafile_a,list) , "it is expected a list"
    assert isinstance(datafile_b,list) , "it is expected a list"
    
    assert datafile_a[0]==path+file_a[0] , "Wrong absolute path assembly"
    

def test_info_from_datasets_defaults():
    
    "Test expected output types and formats"
    
    path='transposonmapper/data_files/files4test/'
    file_a= ['WT_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'WT_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    file_b= ['dnrp1-1_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'dnrp1-1_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    
    datafile_a,datafile_b=make_datafile(path,file_a,path,file_b)
    
    variable = 'read_per_gene' 
    normalize=True
    
    variable_a_array,variable_b_array,_,_,_=info_from_datasets(datafile_a,datafile_b,variable=variable, normalize=normalize)
    
    assert isinstance(variable_a_array,numpy.ndarray) , "It is expected an array"
    assert isinstance(variable_b_array,numpy.ndarray) , "It is expected an array"
    
    assert variable_a_array.shape[1]==len(datafile_a), "The array should have same number of columns as the number of replicates from the library"
    assert variable_b_array.shape[1]==len(datafile_b), "The array should have same number of columns as the number of replicates from the library"


def test_apply_stats():
    
    "Test expected output types and formats"
    
    path='transposonmapper/data_files/files4test/'
    file_a= ['WT_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'WT_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    file_b= ['dnrp1-1_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'dnrp1-1_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    
    datafile_a,datafile_b=make_datafile(path,file_a,path,file_b)
    
    variable = 'read_per_gene' 
    normalize=True
    
    significance_threshold=0.01
    
    variable_a_array,variable_b_array,_,_,volcano_df=info_from_datasets(datafile_a,datafile_b,variable=variable, normalize=normalize)
    
    data2volcano=apply_stats(variable_a_array,variable_b_array,significance_threshold,volcano_df)
    
    assert any("fold_change" in s for s in data2volcano.columns.tolist()), "It needs the fold_change column for the volcano plot"
    assert any("p_value" in s for s in data2volcano.columns.tolist()), "It needs the fold_change column for the volcano plot"
    