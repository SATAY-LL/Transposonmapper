import os
import pkg_resources
import pytest
import numpy as np

import pysam
from transposonmapper.properties import (
    get_chromosome_names,
    get_sequence_length,
)

from transposonmapper.mapping import (
    add_chromosome_length_inserts,
    get_reads
    
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
def coordinates_array(bam):
    """
    Load coordinates array 
    """
    readnumb_array, tncoordinates_array, coordinates_array = get_reads(bam)
    
       
    
    return coordinates_array


@pytest.fixture
def ref_names(bam):
    """
    Load reference name file
    """
    
    ref_tid = get_chromosome_names(bam)
    ref_names = list(ref_tid.keys())
   
    
    return ref_names
    

@pytest.fixture
def chr_len(bam):
    """
    Load input files required to run add_chromosome_length
    """
    
       # Get sequence lengths of all chromosomes
    chr_len, chr_lengths_cumsum = get_sequence_length(bam)
   
    
    return chr_len


def test_output_is_array(coordinates_array, ref_names, chr_len):
    
    coord = add_chromosome_length_inserts(coordinates_array, ref_names, chr_len)
    
    assert isinstance(coord, np.ndarray), "Expected numpy.array type"
