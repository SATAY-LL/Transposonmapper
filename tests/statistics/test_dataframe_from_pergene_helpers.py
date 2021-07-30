import pytest 
import pandas 
import pkg_resources
import os 

from transposonmapper.statistics import read_pergene_file,reads_per_insertion,essential_genes
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

def test_read_pergene_file(bamfile,pergene):

    transposonmapper(bamfile)

    genenames_list,tnpergene_list,readpergene_list,lines=read_pergene_file(pergene)

    assert isinstance(genenames_list,list), "It is expected a list"
    assert isinstance(tnpergene_list,list), "It is expected a list"
    assert isinstance(readpergene_list,list), "It is expected a list"
    assert isinstance(lines,list), "It is expected a list"

    assert len(genenames_list)==len(tnpergene_list)==len(readpergene_list)==len(lines) , "It is expected the same length"


def test_reads_per_insertion(bamfile,pergene):
    
    transposonmapper(bamfile)

    _,tnpergene_list,readpergene_list,lines=read_pergene_file(pergene)

    data=reads_per_insertion(tnpergene_list,readpergene_list,lines)
    
    assert isinstance(data,list), "It is expected a list"
    
    assert len(data)==len(readpergene_list), "It is expected the same length"
    
def test_essential_genes(bamfile,pergene):

    transposonmapper(bamfile)

    genenames_list,_,_,lines=read_pergene_file(pergene)

    essentials=essential_genes(genenames_list,lines)

    assert isinstance(essentials,list) , "It is expected a list"
    assert len(essentials)==len(genenames_list), "It is expected the same length"