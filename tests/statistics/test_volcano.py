from transposonmapper.statistics import volcano
import pandas 

def test_output():
    

    path='transposonmapper/data_files/files4test/'
    file_a= ['WT_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'WT_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    file_b= ['dnrp1-1_merged-DpnII-NlaIII-a_trimmed.sorted.bam_pergene.txt',
 'dnrp1-1_merged-DpnII-NlaIII-b_trimmed.sorted.bam_pergene.txt']
    
    data=volcano(path,file_a,path,file_b,fold_change_interval=[1,-1],p_value_interval=[2,2])
    
    assert  isinstance(data,pandas.core.frame.DataFrame) , "It is expected a dataframe"