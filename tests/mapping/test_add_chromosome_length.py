import os
import pkg_resources
import pytest

import pysam
from transposonmapper.properties import (
    get_chromosome_names,
    get_sequence_length,
)

from transposonmapper.mapping import (
    add_chromosome_length,
    
)

from transposonmapper.utils import chromosomename_roman_to_arabic

from transposonmapper.importing import (
    load_default_files,
    read_genes,
)


@pytest.fixture
def bam():
    """
    Load bamfile for testing
    """
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test/")
    filename = "SRR062634.filt_trimmed.sorted.bam"
    bamfile = os.path.join(data_path, filename)
    bam = pysam.AlignmentFile(bamfile, "rb")  # open bam formatted file for reading
    return bam

@pytest.fixture
def coordinates(bam):
    """
    Load input files required to run add_chromosome_length
    """
    a,b,c=load_default_files(None,None,None)

    gene_coordinates, essential_coordinates, aliases_designation = read_genes(a, b, c)
    
       
    
    return gene_coordinates


@pytest.fixture
def chr_sum(bam):
    """
    Load input files required to run add_chromosome_length
    """
    
    chr_len,chr_sum=get_sequence_length(bam)
   
    
    return chr_sum
    

@pytest.fixture
def ref_tid_roman(bam):
    """
    Load input files required to run add_chromosome_length
    """
    
    ref_tid = get_chromosome_names(bam)
    ref_romannums = chromosomename_roman_to_arabic()[1]
    ref_tid_roman = {key: value for key, value in zip(ref_romannums, ref_tid)}
   
    
    return ref_tid_roman
    

def test_output_is_dict(coordinates,chr_sum,ref_tid_roman):
    
    coord = add_chromosome_length(coordinates,chr_sum,ref_tid_roman)
    
    assert isinstance(coord, dict), "Expected dict type"


