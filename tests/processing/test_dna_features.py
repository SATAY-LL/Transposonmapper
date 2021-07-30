
import os
import pkg_resources
import pandas
import pytest
from transposonmapper.processing import dna_features, feature_position
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
def wigfile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.wig"
    wigfile = os.path.join(datapath, data_file)
    return wigfile 

@pytest.fixture
def per_gene_insertions(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam_pergene_insertions.txt"
    per_gene_insertions = os.path.join(datapath, data_file)
    return per_gene_insertions


def test_output_dna_features(bamfile,wigfile,per_gene_insertions):
    
    transposonmapper(bamfile)
    
    region='I'
    dna_output=dna_features(region=region,wig_file=wigfile,pergene_insertions_file=per_gene_insertions)
    
    assert isinstance(dna_output, pandas.core.frame.DataFrame) , " It is expected a dataframe"
    

    