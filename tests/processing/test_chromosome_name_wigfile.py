import os
import pkg_resources
import pytest

from transposonmapper.processing.chromosome_names_in_files import chromosome_name_wigfile

@pytest.fixture
def wigfile():
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    data_file = "SRR062634.filt_trimmed.sorted.bam.wig"
    wigfile = os.path.join(data_path, data_file)
    return wigfile
    
def test_output_type_data(wigfile):
    """Test default arguments and outputs type and content """


    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_wigfile(wig_file=wigfile)

    assert isinstance(chrom_names_dict, dict), "Expected dict type"
    assert isinstance(chrom_start_line_dict, dict), "Expected dict type"
    assert isinstance(chrom_end_line_dict, dict), "Expected dict type"


def test_output_len_data(wigfile):
    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_wigfile(wig_file=wigfile)

    assert len(chrom_names_dict)==17 , "Expected 16 chromosomes + 1 Mitocondrial chromosome in yeast"
    assert len(chrom_start_line_dict)==17 , "Expected 16 chromosomes + 1 Mitocondrial chromosome in yeast"
    assert len(chrom_end_line_dict)==17 , "Expected 16 chromosomes + 1 Mitocondrial chromosome in yeast"

def test_output_format_data(wigfile):
    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_wigfile(wig_file=wigfile)
    assert chrom_names_dict['I']=='ref|NC_001133|', " Expected different name"
    assert isinstance(chrom_start_line_dict['I'],int), "Expected an integer value"
    assert isinstance(chrom_end_line_dict['I'],int), "Expected an integer value"
    # -*- coding: utf-8 -*-

