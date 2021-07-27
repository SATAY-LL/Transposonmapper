import os
import pkg_resources
from transposonmapper.utils import chromosomename_roman_to_arabic
from transposonmapper.importing import load_default_files,load_sgd_tab
from transposonmapper.properties import list_gene_names , gene_position, gene_aliases,chromosome_position
from transposonmapper.processing import chromosome_name_wigfile
from transposonmapper.processing.read_sgdfeatures import sgd_features   


def input_region(region,verbose):
    """Defines the region of interest for further processing 

    Parameters
    ----------
    region : str, int or list
        Enter chromosome as a number (or roman numeral) between 1 and 16 (I and XVI), 
        a list in the form ['chromosome number, start_position, end_position'] or a valid gene name.
    verbose : bool
        To allow warning messages. 
    

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




def read_wig_file(wig_file,chrom):
    """Extract the information in the wigfile related to the chromosome of interested

    Parameters
    ----------
    wig_file : str
        absolute path of the wigfile location
    chrom : str
        Name of the chromosome in roman where to extract the informatiion from the wigfile

    Returns
    -------
    insrt_in_chrom_list : list 
        Genomic locations of transposon insertions in the given chromosome.
    reads_in_chrom_list: list
        How many reads are in each of the genomic locations of the insertions. 
    
    """

    with open(wig_file, 'r') as f:
        lines = f.readlines()

    chrom_start_line_dict, chrom_end_line_dict = chromosome_name_wigfile(lines)[1:]

    insrt_in_chrom_list = []
    reads_in_chrom_list = []
    for l in lines[chrom_start_line_dict.get(chrom):chrom_end_line_dict.get(chrom)]:
        insrt_in_chrom_list.append(int(l.strip('\n').split(' ')[0]))
        reads_in_chrom_list.append(int(l.strip('\n').split(' ')[1]))
        
    return insrt_in_chrom_list,reads_in_chrom_list


def read_pergene_file(pergene_insertions_file,chrom):
    """Reading the pergene file , the information per gene , related to where it starts and ends in the genome. 

    Parameters
    ----------
    pergene_insertions_file : str
        absolute path of the per gene file location
    chrom : str
        Name of the chromosome in roman where to extract the informatiion from the wigfile

    Returns
    -------
    gene_position_dict : dict 
        A dictionary describing the chromosome, start, and end location of every gene in the chromosome of interest. 
    """

    with open(pergene_insertions_file) as f:
        lines = f.readlines()


    gene_position_dict = {}
    for line in lines[1:]:
        line_split = line.strip('\n').split('\t')


        if line_split[1] == chrom:
            genename = line_split[0]
            gene_chrom = line_split[1]
            gene_start = int(line_split[2])
            gene_end = int(line_split[3])

            gene_position_dict[genename] = [gene_chrom, gene_start, gene_end] #DICT CONTAINING ALL GENES WITHIN THE DEFINED CHROMOSOME INCLUDING ITS START AND END POSITION


            geneinserts_str = line_split[4].strip('[]')
            if not geneinserts_str == '':
                geneinserts_list = [int(ins) for ins in geneinserts_str.split(',')]
            else:
                geneinserts_list = []


            genereads_str = line_split[5].strip('[]')
            if not genereads_str == '':
                genereads_list = [int(read) for read in genereads_str.split(',')]
            else:
                genereads_list = []


            if len(geneinserts_list) != len(genereads_list):
                print('WARNING: %s has different number of reads compared with the number of inserts' % genename )

    return gene_position_dict


def gene_location(chrom,gene_position_dict,verbose):
    """It gives structured information from the genes inside the chromosome of interest

    Parameters
    ----------
    chrom : str
        Name of the chromosome in roman where to extract the informatiion from the wigfile
    gene_position_dict : dict
        Dictionary with info of the genes inside the chromosome . It is the output of the function
        read_pergene_file

    verbose : bool 
        Same as main function dna_features. If True allows for warning messages. 

    Returns
    -------
    dna_dict: dict
        Dictionary with info about genes encoded in the sgd features file 
    start_ch : int
        Integer indicating the genomic location of where the chromosome of interest starts
    end_chr: int 
        Integer indicating the genomic location of where the chromosome of interest ends
    len_chr: int
        Length of the chromosome of interest
    feature_orf_dict: dict
        Dictionary with info about genes in the chromosome of interest 
    """

    gff_file,_,gene_information_file=load_default_files()
    sgd_features_file=load_sgd_tab()
    

    len_chr = chromosome_position(gff_file)[0].get(chrom)
    start_chr = chromosome_position(gff_file)[1].get(chrom)
    end_chr = chromosome_position(gff_file)[2].get(chrom)
    if verbose == True:
        print('Chromosome length = ', len_chr)

    dna_dict = {} #for each bp in chromosome, determine whether it belongs to a noncoding or coding region
    for bp in range(start_chr, end_chr + 1): #initialize dna_dict with all basepair positions as ['noncoding', None]
        dna_dict[bp] = ['noncoding', None] #form is: ['element_name', 'type']


    feature_orf_dict = sgd_features(sgd_features_file)[1]
    gene_alias_dict = gene_aliases(gene_information_file)[0]


    for gene in gene_position_dict:
        if gene in feature_orf_dict:
            if (not gene.endswith("-A") and not feature_orf_dict.get(gene)[1] == 'Verified') and (not gene.endswith("-B") and not feature_orf_dict.get(gene)[1] == 'Verified'):
                for bp in range(gene_position_dict.get(gene)[1]+start_chr, gene_position_dict.get(gene)[2]+start_chr+1):
                    dna_dict[bp] = [gene, "Gene; "+feature_orf_dict.get(gene)[1]]
        else:
            gene_alias = [key for key, val in gene_alias_dict.items() if gene in val][0]
            for bp in range(gene_position_dict.get(gene)[1]+start_chr, gene_position_dict.get(gene)[2]+start_chr+1):
                dna_dict[bp] = [gene_alias, "Gene; "+feature_orf_dict.get(gene_alias)[1]]

    return dna_dict,start_chr,end_chr,len_chr,feature_orf_dict