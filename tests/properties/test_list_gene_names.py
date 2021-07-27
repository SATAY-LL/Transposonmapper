from transposonmapper.properties.list_gene_names import list_gene_names 

def test_output_data():
    
    genes_names=list_gene_names()
    
    assert isinstance(genes_names,list) , "The gene names should be in a list"
    
    for i in genes_names: 
        assert isinstance(i,str) , "Every gene should be a string "
