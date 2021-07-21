import os
import pkg_resources
import pytest

from transposonmapper.processing.chromosome_names_in_files import chromosome_name_bedfile

@pytest.fixture
def bedfile():
    data_path = pkg_resources.resource_filename("transposonmapper", "data_files/files4test")
    data_file = "SRR062634.filt_trimmed.sorted.bam.bed"
    bedfile = os.path.join(data_path, data_file)
    return bedfile 
    
def test_output_type_data(bedfile):
    """Test default arguments and outputs type and content """


    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_bedfile(bed_file=bedfile)

    assert isinstance(chrom_names_dict, dict), "Expected dict type"
    assert isinstance(chrom_start_line_dict, dict), "Expected dict type"
    assert isinstance(chrom_end_line_dict, dict), "Expected dict type"


def test_output_len_data(bedfile):
    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_bedfile(bed_file=bedfile)

    assert len(chrom_names_dict)==16 , "Expected 16 chromosomes in yeast"
    assert len(chrom_start_line_dict)==16 , "Expected 16 chromosomes in yeast"
    assert len(chrom_end_line_dict)==16 , "Expected 16 chromosomes in yeast"

def test_output_format_data(bedfile):
    chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_bedfile(bed_file=bedfile)
    assert chrom_names_dict['I']=='ref|NC_001133|', " Expected different name"
    assert isinstance(chrom_start_line_dict['I'],int), "Expected an integer value"
    assert isinstance(chrom_end_line_dict['I'],int), "Expected an integer value"
    
    