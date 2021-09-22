import os
import pkg_resources

def load_default_files(gff_file=None, essentials_file=None, gene_names_file=None):
    """This function loads some files that have a recurrent use throughout the pipeline.
    It will look inside the satay/data_files folder for the files if the input is None. 
    Otherwise it will return the same input file.  
    


    Parameters
    ----------
    gff_file : .gff3, optional
         Annotated genome from Saccharomyces cerevisiae (baker's yeast) 
        (https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz), by default None
    essentials_file : .txt, optional
        Essentials genes annotated from yeast , written using the systematic name standard , 
        all in one column, by default None
    gene_names_file : .txt, optional
        This documents lists all the Saccharomyces cerevisiae S288c entries present in
        this release of UniProtKB/Swiss-Prot. Yeast (Saccharomyces cerevisiae): entries, 
        gene names and cross-references to SGD. 
        Release:     2021_01 of 10-Feb-2021, by default None

    Returns
    -------
    str: 

        The correct path of the .gff3 input required file for the further analysis. 
    str: 

        The correct path of the essential file input required file for the further analysis. 
    str: 

        The correct path of the gene_name_file required file for the further analysis.
    """

    default_path = pkg_resources.resource_filename("transposonmapper", "data_files/")
    if gff_file is None:
        gff_file = os.path.join(
            default_path, "Saccharomyces_cerevisiae.R64-1-1.99.gff3"
        )
    if essentials_file is None:
        essentials_file = os.path.join(
            default_path, "Cerevisiae_AllEssentialGenes_List.txt"
        )
    if gene_names_file is None:
        gene_names_file = os.path.join(default_path, "Yeast_Protein_Names.txt")


    return gff_file, essentials_file, gene_names_file


def load_sgd_tab(sgd_features_file=None):
    """This function loads the file SGD_features.tab
    The latest version of the SGD_features.tab file is based on Genome Version R64-2-1.
    If a specific file is provided it will output that file , otherwise , if it is set to None then 
    it will give the standard file provided in the package. 
        
   

    Parameters
    ----------
    sgd_features_file : str, optional
        The latest version of the SGD_features.tab file is based on Genome Version R64-2-1., by default None

    Returns
    -------
    str: 
        The path corresponding to this file in the package 
    """
    default_path = pkg_resources.resource_filename("transposonmapper", "data_files/")
    if sgd_features_file is None: 

        sgd_features_file = os.path.join(default_path,'SGD_features.tab')

    return sgd_features_file

