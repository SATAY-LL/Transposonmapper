import os
from transposonmapper.importing import load_sgd_tab
from transposonmapper.utils   import  chromosomename_roman_to_arabic

from transposonmapper.processing.read_sgdfeatures import sgd_features

def test_output():
    
    a=sgd_features()[0]
    b=sgd_features()[1]
    assert isinstance(a,list) , "The genomic regions should be in a list"
    assert len(a)==20 , "There should be 20 genomic regions"
    

    assert isinstance(b, dict) , "The features from all ORF should be a dict"
    assert len(b)>=6000 , "The number of ORFs in yeast should be more than 6000"


