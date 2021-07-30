from transposonmapper.processing.essential_genes_names import list_known_essentials
from transposonmapper.importing import load_default_files
from transposonmapper.properties.get_chromosome_position import chromosome_position
import pytest

@pytest.fixture
def essential_file():
    _, essential_file, _ = load_default_files(
        gff_file=None, essentials_file=None, gene_names_file=None
    )
    return essential_file

def test_output_data(essential_file):
    

    genes_essential_list = list_known_essentials(essential_file)
    
    assert isinstance(genes_essential_list,list) , "The essential genes list should inside a list"
    
    for i in genes_essential_list:
        assert(type(i)==str), "Each of the genes should be strings"