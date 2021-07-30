import pytest 
import pandas 
import pkg_resources
import os 

from transposonmapper.statistics import dataframe_from_pergenefile
from transposonmapper import transposonmapper

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
def pergene(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam_pergene.txt"
    pergene = os.path.join(datapath, data_file)
    return pergene


def test_output(bamfile,pergene):
    
    transposonmapper(bamfile)
    
    data=dataframe_from_pergenefile(pergene)
    
    assert isinstance(data,pandas.core.frame.DataFrame), "It is expected a dataframe"

def test_format(bamfile,pergene):
    transposonmapper(bamfile)
    
    data=dataframe_from_pergenefile(pergene)
    
    with open(pergene) as f:
        lines = f.readlines()[1:] #skip header
        
    assert len(lines)==len(data) , "It is expected the same genes as the ones indicated in the file"