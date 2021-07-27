import os
import pkg_resources
import glob
import pandas as pd

import pytest
import numpy 


from transposonmapper import transposonmapper

from transposonmapper.processing import input_region
from transposonmapper.utils import chromosomename_roman_to_arabic

def test_output_chrom():
    
    region=['I', 1]
    for region in region: 
        roi_start,roi_end,region_type,chrom=input_region(region=region)
        
        if type(region)==str or type(region)==int:
        
            assert region_type=='Chromosome', "It should be a chromosome according the region provided"
            
    
       
        
        if region in chromosomename_roman_to_arabic()[0]:
            "if region is an int"
            chrom_new=chromosomename_roman_to_arabic()[0].get(region)
    
            assert chrom_new==chrom , "Not correct conversion between arabic and roman"

        else: 
             region==chrom, "It should be roman "
    
    
def test_output_gene():

    region='cdc42'

    roi_start,roi_end,region_type,chrom=input_region(region=region)
        
        
    assert region_type=='Gene', "It should be a Gene according the region provided"
            
    assert type(roi_start)==int, "It should be the start position of the gene in the genome, as an integer"
    assert type(roi_end)==int, "It should be the end position of the gene in the genome, as an integer"

    assert type(chrom)==str, "It should give the name of the chromosome of the gene of interest"