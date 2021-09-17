import os

import pkg_resources
import glob
import pandas 

import pytest
import numpy 


from transposonmapper import transposonmapper
from transposonmapper.properties.gene_aliases import gene_aliases
from transposonmapper.processing import (input_region,read_pergene_file,
read_wig_file,gene_location,feature_position,intergenic_regions, build_dataframe)
from transposonmapper.utils import chromosomename_roman_to_arabic



@pytest.fixture
def bamfile():
    """
    Load bamfile for testing
    """
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test/")
    filename = "SRR062634.filt_trimmed.sorted.bam"
    bamfile = os.path.join(data_path, filename)
    
    return bamfile

@pytest.fixture
def datapath():
    datapath = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    return datapath

@pytest.fixture
def wigfile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.wig"
    wigfile = os.path.join(datapath, data_file)
    return wigfile 

@pytest.fixture
def pergenefile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam_pergene_insertions.txt"
    pergenefile = os.path.join(datapath, data_file)
    return pergenefile 


def test_output_chrom_input_region():
    
    region=['I', 1]
    for region in region: 
        _,_,region_type,chrom=input_region(region=region,verbose=True)
        
        if type(region)==str or type(region)==int:
        
            assert region_type=='Chromosome', "It should be a chromosome according the region provided"
            
    
       
        
        if region in chromosomename_roman_to_arabic()[0]:
            "if region is an int"
            chrom_new=chromosomename_roman_to_arabic()[0].get(region)
    
            assert chrom_new==chrom , "Not correct conversion between arabic and roman"

        else: 
             region==chrom, "It should be roman "
    
    
def test_output_gene_input_region():

    region='cdc42'

    roi_start,roi_end,region_type,chrom=input_region(region=region,verbose=True)
        
        
    assert region_type=='Gene', "It should be a Gene according the region provided"
            
    assert type(roi_start)==int, "It should be the start position of the gene in the genome, as an integer"
    assert type(roi_end)==int, "It should be the end position of the gene in the genome, as an integer"

    assert type(chrom)==str, "It should give the name of the chromosome of the gene of interest"

def test_output_read_wig_file(bamfile,wigfile):

    transposonmapper(bamfile)
    chrom='I'
    insertions, reads=read_wig_file(wigfile,chrom)
    
    assert isinstance(insertions,list), "The insertions in the region of interest are a list"
    assert isinstance(reads,list), "The reads in the region of interest are a list"


def test_output_pergene_file(bamfile,pergenefile):

    transposonmapper(bamfile)
    chrom='I'
    gene_locations=read_pergene_file(pergenefile,chrom)
    
    assert isinstance(gene_locations,dict) , "It is expected a dictionary"
    
    assert any(chrom in val for val in gene_locations.values()) , "The chromosome name should be in the values of the dictionary"


def test_output_gene_location(bamfile, pergenefile):

    transposonmapper(bamfile)
    chrom='I'
    gene_dict=read_pergene_file(pergenefile,chrom)
    
    dna_dict,start_chr,end_chr,len_chr,feature_orf_dict=gene_location(chrom,gene_dict,verbose=True)

    
    assert isinstance(dna_dict,dict) , "It is expected a dictionary"
    
    assert isinstance(start_chr,int), "It is expected an integer"
    
    assert isinstance(end_chr,int), "It is expected an integer"
    
    assert isinstance(len_chr,int) , "Its is expected an integer"
    
    assert isinstance(feature_orf_dict,dict) , "It is expected a dictionary"
    
   

def test_output_feature_position():
    
    chrom='I'
    value=[1,2,3,4,5,chrom,6,7,8,9,10]
    dict_toy=dict.fromkeys(range(10), value)
    
    dna_dict=feature_position(dict_toy, chrom, 0, dict_toy, feature_type=None)
    
    assert isinstance(dna_dict,dict) , "It is expected a dictionary"
    
    assert len(dna_dict)==len(dict_toy), "It is expected same length"
    
    
def test_output_intergenic_regions(pergenefile,bamfile):
    
    transposonmapper(bamfile)
    chrom="I"
    gene_position_dict=read_pergene_file(pergenefile,chrom=chrom)
    
    dna_dict,start_chr,_,_,_=gene_location(chrom,gene_position_dict,verbose=True)
    
    dna_dict_new2,genomicregions_list=intergenic_regions(chrom,start_chr,dna_dict)
    
    assert isinstance(dna_dict_new2,dict) , "It is expected a dictionary"
    assert isinstance(genomicregions_list,list) , "It is expected a list"
    
    
def test_output_build_dataframe(pergenefile,bamfile,wigfile):

    transposonmapper(bamfile)
    chrom="V"
    insrt_in_chrom_list, reads_in_chrom_list=read_wig_file(wigfile,chrom)
    gene_position_dict=read_pergene_file(pergenefile,chrom=chrom)
    
    dna_dict,start_chr,end_chr,_,_=gene_location(chrom,gene_position_dict,verbose=True)
    
    dna_dict,genomicregions_list=intergenic_regions(chrom,start_chr,dna_dict)

    dataf=build_dataframe(dna_dict,start_chr,end_chr,insrt_in_chrom_list,reads_in_chrom_list,genomicregions_list,chrom)

    assert isinstance(dataf,pandas.core.frame.DataFrame) , "It is expected a dataframe"

    