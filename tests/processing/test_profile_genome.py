import os
import numpy 
import pkg_resources

import pytest 
from transposonmapper import transposonmapper
from transposonmapper.importing import load_default_files
from transposonmapper.properties.get_chromosome_position import chromosome_position
from transposonmapper.processing.transposonread_profileplot_genome import profile_genome
from transposonmapper.processing.profileplot_genome_helpers import length_genome

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
def datapath():
    datapath = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    return datapath

@pytest.fixture
def bedfile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.bed"
    bedfile = os.path.join(datapath, data_file)
    return bedfile 

def test_length_genome(chr_input):
    """Checking type of output data"""

    l_genome=length_genome(chr_input)
    
    assert isinstance(l_genome,int) , "The length of the genome should be an integer"

def test_output_data(bedfile,bamfile,chr_input):
    
    transposonmapper(bamfile)
    genome=length_genome(chr_input)
    bins=1000
    a,b=profile_genome(bedfile,bar_width=genome/bins)

    

    
    assert isinstance(a,numpy.ndarray) , "It should be an array of float64"
    assert isinstance(b,list) , "It should be a list"
    assert len(a)==len(b)==bins+1 , "It should have equal lengths both variable"