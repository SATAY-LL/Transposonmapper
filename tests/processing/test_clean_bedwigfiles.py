import os
import pkg_resources
import glob
import pandas as pd

import pytest

from transposonmapper.processing.clean_bedwigfiles import cleanfiles
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
def bedfile(datapath):
   
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.bed"
    bedfile = os.path.join(datapath, data_file)
    return bedfile 

@pytest.fixture
def wigfile(datapath):
    
    data_file = "SRR062634.filt_trimmed.sorted.bam.wig"
    wigfile = os.path.join(datapath, data_file)
    return wigfile


def test_output_data(bamfile,wigfile,bedfile,datapath):

    transposonmapper(bamfile)
    cleanfiles(filepath=wigfile,custom_header="", split_chromosomes=False)
    cleanfiles(filepath=bedfile,custom_header="", split_chromosomes=False)
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)
    file_bed = glob.glob(datapath + "/**/*" + "_clean.bed", recursive=True)
    
    assert len(file_wig)>=1, "There is a clean file per wigfile"
    assert len(file_bed)>=1, "There is a clean file per bedfile"


def test_empty_custom_header_bed(bamfile,bedfile,datapath):
    
    transposonmapper(bamfile)
    cleanfiles(filepath=bedfile,custom_header="", split_chromosomes=False)
    
    with open(bedfile, "r") as f:
            lines = f.readlines()
            
    
    file_bed = glob.glob(datapath + "/**/*" + "_clean.bed", recursive=True)

    data = pd.read_csv(file_bed[0], delimiter="\t")

    assert data.columns[0]==lines[0].strip('\n') , "Expect a different name when custom header is empty"


def test_empty_custom_header_wig(bamfile,wigfile,datapath):
    
    transposonmapper(bamfile)
    cleanfiles(filepath=wigfile,custom_header="", split_chromosomes=False)
    
    with open(wigfile, "r") as f:
            lines = f.readlines()
             
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)

    data = pd.read_csv(file_wig[0], delimiter="\t")

    assert data.columns[0]==lines[0].replace(',','').strip('\n'), "Expect a different name when custom header is empty"
    

def test_nonempty_custom_header_wig(bamfile,wigfile,datapath):

    transposonmapper(bamfile)
    
    custom_header="test_name"

    cleanfiles(filepath=wigfile,custom_header=custom_header, split_chromosomes=False)
    
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)

    data = pd.read_csv(file_wig[0], delimiter="\t")

    assert data.columns[0]=="track type=wiggle_0 maxheightPixels=60 name=" + str(custom_header), "Expect a different name when custom header is nonempty"
