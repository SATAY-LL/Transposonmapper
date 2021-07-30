import os
from transposonmapper.importing import load_sgd_tab
from transposonmapper.utils   import  chromosomename_roman_to_arabic

from transposonmapper.processing.read_sgdfeatures import sgd_features

def test_output():
    
    a=sgd_features()
    
    
    
    assert isinstance(a[0],list) , "The genomic regions should be in a list"
    assert len(a[0])>=20 , "There should be  20 genomic regions"
    

    assert isinstance(a[1], dict) , "The features from all ORF should be a dict"
    assert len(a[1])>=6000 , "The number of ORFs in yeast should be more than 6000"


