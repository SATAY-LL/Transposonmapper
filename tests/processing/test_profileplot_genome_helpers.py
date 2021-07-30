import os
import pkg_resources
import glob
import pandas as pd

import pytest
import numpy 
from transposonmapper.importing import load_default_files
from transposonmapper.properties.get_chromosome_position import chromosome_position
from transposonmapper import transposonmapper
from transposonmapper.processing import summed_chr,counts_genome,length_genome,binned_list,middle_chrom_pos

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
def gff_file():
    gff_file, _, _ = load_default_files(
        gff_file=None, essentials_file=None, gene_names_file=None
    )
    return gff_file

@pytest.fixture
def chr_input(gff_file):
    chr_input, _, _ = chromosome_position(gff_file)

    return chr_input

@pytest.fixture
def bedfile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.bed"
    bedfile = os.path.join(datapath, data_file)
    return bedfile 

def test_summed_chr(chr_input):
    """Checking type of output data"""
   
    a=summed_chr(chr_input)

    assert len(a)==16 , "There are 16 chromosomes summed "
    
    assert isinstance(a['I'],int), "The sum should be an integer"
    
def test_length_genome(chr_input):
    """Checking type of output data"""

    l_genome=length_genome(chr_input)
    
    assert isinstance(l_genome,int) , "The length of the genome should be an integer"
   
def test_middle_chrom_pos(chr_input):
    """Checking type of output data"""

    middle_chr_position=middle_chrom_pos(chr_input)
    
    assert len(middle_chr_position)==16 , "There are 16 chromosomes to analyze in yeast"
    assert isinstance(middle_chr_position,list), "The output should be a list"
    

def test_counts_genome(gff_file,bamfile,bedfile,chr_input):
    """Checking type of output data"""
    
    variable="transposons"

    transposonmapper(bamfile)
    
    l_genome=length_genome(chr_input) # length of the genome
    
    allcounts_list=counts_genome(variable,bedfile,gff_file)
    
    assert type(allcounts_list)==numpy.ndarray, "The counts of the genome output should be an array "
    
    assert len(allcounts_list)==l_genome , " The array should have a length equal to the length of the genome"

def test_binned_list(bedfile,gff_file,bamfile,chr_input):
    variable="transposons"

    transposonmapper(bamfile)
    l_genome=length_genome(chr_input) # length of the genome
    
    allcounts_list=counts_genome(variable,bedfile,gff_file)
    bins=1000

    allcounts_binnedlist=binned_list(allcounts_list,bar_width= l_genome/bins)
    
    assert isinstance(allcounts_binnedlist,list), "It has to be a list"
    
    assert len(allcounts_binnedlist)==bins+1 , "The length should be number of bins+1"
