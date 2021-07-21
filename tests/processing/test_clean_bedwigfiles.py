import os
import pkg_resources
import glob
import pandas as pd
import pytest

from transposonmapper.processing.clean_bedwigfiles import cleanfiles

@pytest.fixture
def datapath():
    datapath = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    return datapath

@pytest.fixture
def bedfile():
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    data_file = "SRR062634.filt_trimmed.sorted.bam.bed"
    bedfile = os.path.join(data_path, data_file)
    return bedfile 

@pytest.fixture
def wigfile():
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    data_file = "SRR062634.filt_trimmed.sorted.bam.wig"
    wigfile = os.path.join(data_path, data_file)
    return wigfile


def test_output_data(wigfile,bedfile,datapath):
    
    cleanfiles(filepath=wigfile,custom_header="", split_chromosomes=False)
    cleanfiles(filepath=bedfile,custom_header="", split_chromosomes=False)
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)
    file_bed = glob.glob(datapath + "/**/*" + "_clean.bed", recursive=True)
    
    assert len(file_wig)>=1, "There is a clean file per wigfile"
    assert len(file_bed)>=1, "There is a clean file per bedfile"


def test_empty_custom_header_bed(bedfile,datapath):
    

    cleanfiles(filepath=bedfile,custom_header="", split_chromosomes=False)
    
    with open(bedfile, "r") as f:
            lines = f.readlines()
            
    
    file_bed = glob.glob(datapath + "/**/*" + "_clean.bed", recursive=True)

    data = pd.read_csv(file_bed[0], delimiter="\t")

    assert data.columns[0]==lines[0].strip('\n') , "Expect a different name when custom header is empty"


def test_empty_custom_header_wig(wigfile,datapath):
    

    cleanfiles(filepath=wigfile,custom_header="", split_chromosomes=False)
    
    with open(wigfile, "r") as f:
            lines = f.readlines()
             
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)

    data = pd.read_csv(file_wig[0], delimiter="\t")

    assert data.columns[0]==lines[0].replace(',','').strip('\n'), "Expect a different name when custom header is empty"
    

def test_nonempty_custom_header_wig(wigfile,datapath):
    
    custom_header="test_name"

    cleanfiles(filepath=wigfile,custom_header=custom_header, split_chromosomes=False)
    
    
    file_wig = glob.glob(datapath + "/**/*" + "_clean.wig", recursive=True)

    data = pd.read_csv(file_wig[0], delimiter="\t")

    assert data.columns[0]=="track type=wiggle_0 maxheightPixels=60 name=" + str(custom_header), "Expect a different name when custom header is nonempty"
