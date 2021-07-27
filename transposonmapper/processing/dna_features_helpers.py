import os
import pkg_resources
from transposonmapper.utils import chromosomename_roman_to_arabic
from transposonmapper.importing import load_default_files
from transposonmapper.properties import list_gene_names , gene_position, gene_aliases

def input_region(region,verbose=True):
    """Defines the region of interest for further processing 

    Parameters
    ----------
    region : str, int or list
        Enter chromosome as a number (or roman numeral) between 1 and 16 (I and XVI), 
        a list in the form ['chromosome number, start_position, end_position'] or a valid gene name.
    verbose : bool, optional
        To allow warning messages, by default True
    

    Returns
    -------
    roi_start : NoneType, int 
        Describe the start of the genomic location if region=gene name , otherwise is a NoneType
    roi_end : NoneType, int 
        Describe the  end of the genomic location if region=gene name , otherwise is a NoneType

    region_type: str
        It is either "Gene" or "Chromosome" depending on the region provided
    chrom: str
        It is the name of the chromosome of the gene of interest if a gene name is provided as the region, otherwise
        is the roman description of the chromosome of interest. 
    """
    
    gff_file,_,gene_information_file=load_default_files()

    warningmessage = "WARNING: Specified chromosome or gene name not found. Enter chromosome as a number (or roman numeral) between 1 and 16 (I and XVI), a list in the form ['chromosome number, start_position, end_position'] or a valid gene name."

    
    if verbose == True:
        print('Selected region: ', region)

    if type(region) == str:
        if region.upper() in chromosomename_roman_to_arabic()[1]:
            chrom = region.upper()
            roi_start = None
            roi_end = None
            region_type = 'Chromosome'

        elif region.upper() in list_gene_names(gene_information_file):
            gene_pos_dict = gene_position(gff_file)
            region = region.upper()
            region_type='Gene'
            if region in gene_pos_dict:
                region_pos = gene_pos_dict.get(region)
                chrom = region_pos[0]
                roi_start = int(region_pos[1])
                roi_end = int(region_pos[2])
            else:
                gene_alias_dict = gene_aliases(gene_information_file)[0]
                region_alias = [key for key, val in gene_alias_dict.items() if region in val]
                if not region_alias == [] and region_alias[0] in gene_pos_dict:
                    region_pos = gene_pos_dict.get(region_alias[0])
                    chrom = region_pos[0]
                    roi_start = int(region_pos[1])-100
                    roi_end = int(region_pos[2])+100
                    
                else:
                    print(warningmessage)
                    return()
            
            

        else:
            print(warningmessage)
            return()


    elif type(region) == list:
        if type(region[0]) == str:
            chrom = region[0].upper()
        elif type(region[0]) == int:
            if region[0] in chromosomename_roman_to_arabic()[0]:
                chrom = chromosomename_roman_to_arabic()[0].get(region[0])
        else:
            print(warningmessage)
            return()
        roi_start = region[1]
        roi_end = region[2]
        region_type = 'Chromosome'


    elif type(region) == int:
        if region in chromosomename_roman_to_arabic()[0]:
            chrom = chromosomename_roman_to_arabic()[0].get(region)
            roi_start = None
            roi_end = None
        else:
            print(warningmessage)
            return()
        region_type = 'Chromosome'


    else:
        print(warningmessage)
        return()
    
    return roi_start,roi_end,region_type,chrom