import os
from transposonmapper.mapping.concatenate_chromosomes import add_chromosome_length_inserts
import pkg_resources
import pytest

import pysam
from transposonmapper.properties import (
    get_chromosome_names,
    get_sequence_length,
)

from transposonmapper.mapping import (
    add_chromosome_length,
    add_chromosome_length,
    get_reads,
    get_insertions_and_reads,
    
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

@pytest.fixture
def coord(coordinates,chr_sum,ref_tid_roman):
    """
    Load input files required to run get_insertions_and_reads
    """
    
    coord = add_chromosome_length(coordinates,chr_sum,ref_tid_roman)
   
    
    return coord


@pytest.fixture
def coordinates_array(bam):
    """
    Load coordinates array 
    """
    readnumb_array, tncoordinates_array, coordinates_array = get_reads(bam)
    
       
    
    return coordinates_array

@pytest.fixture
def readnumb_array(bam):
    """
    Load coordinates array 
    """
    readnumb_array, tncoordinates_array, coordinates_array = get_reads(bam)
    
       
    
    return readnumb_array


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

@pytest.fixture
def coord_inserts(coordinates_array,ref_names,chr_len):
    """
    Load input files required to run get_insertions_and_reads
    """
    
    coord_inserts = add_chromosome_length_inserts(coordinates_array,ref_names,chr_len)
   
    
    return coord_inserts
 
def test_output_is_dict(coord,coord_inserts,readnumb_array):
    
    tn,reads,tn_cooord=get_insertions_and_reads(coord, coord_inserts, readnumb_array)
    
    assert isinstance(tn, dict), "Expected dict type"
    