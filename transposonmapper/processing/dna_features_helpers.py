import os
import pkg_resources
import numpy as np
import pandas as pd 
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
        Name of the chromosome in roman where to extract the information.
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


def feature_position(feature_dict, chrom, start_chr, dna_dict, feature_type=None):
    """ Get features for every gene in the chromosome of interest 

    Parameters
    ----------
    feature_dict : dict
        output of sgd_features(sgd_features_file)[i]
    chrom : str
        Name of the chromosome in roman where to extract the information.
    start_chr : int
        [description]
    dna_dict : dict 
        first output of the gene_location function 
    feature_type : [type], optional
        [description], by default None

    Returns
    -------
     dict 

    """
    
    position_dict = {}
    for feat in feature_dict:
        if feature_dict.get(feat)[5] == chrom:
#            if feat.startswith("TEL") and feat.endswith('L'): #correct for the fact that telomeres at the end of a chromosome are stored in the reverse order.
            if int(feature_dict.get(feat)[6]) > int(feature_dict.get(feat)[7]):
                position_dict[feat] = [feature_dict.get(feat)[5], feature_dict.get(feat)[7], feature_dict.get(feat)[6]]
            else:
                position_dict[feat] = [feature_dict.get(feat)[5], feature_dict.get(feat)[6], feature_dict.get(feat)[7]]


    for feat in position_dict:
        for bp in range(int(position_dict.get(feat)[1])+start_chr, int(position_dict.get(feat)[2])+start_chr):
            if bp in dna_dict:
                if dna_dict[bp] == ['noncoding', None]:
                    dna_dict[bp] = [feat, feature_type]
            else: 
                dna_dict[bp]=[feat, feature_type]


    return(dna_dict)


def intergenic_regions(chrom,start_chr,dna_dict):
    """Getting intergenic regions from chromosome of interest 

    Parameters
    ----------
    chrom : str
        Name of the chromosome in roman where to extract the information.
    start_chr : int
       2nd output of the gene_location function 
    dna_dict : dict 
        1st output of the gene_location function 

    Returns
    -------
    dna_dict_new : dict
        
    genomicregions_list: list

    
    """


    sgd_features_file=load_sgd_tab()
    ## GET FEATURES FROM INTERGENIC REGIONS 

    genomicregions_list = sgd_features(sgd_features_file)[0]

    i = 2
    for genomicregion in genomicregions_list[1:]:
        dna_dict_new = feature_position(sgd_features(sgd_features_file)[i], chrom, start_chr, dna_dict, genomicregion)
        i += 1
    
    return dna_dict_new,genomicregions_list


def checking_features(feature_orf_dict,chrom,gene_position_dict,verbose):
    """ Checking input values 

    Parameters
    ----------
    feature_orf_dict : dict 
        last output of the gene_location function 
    chrom : str
        Name of the chromosome in roman where to extract the information.
    gene_position_dict : dict
        output of the read_pergene_file function 
    verbose : bool 
        If True it allows for warning messages 
    """

    ### TEST IF ELEMENTS IN FEATURE_ORF_DICT FOR SELECTED CHROMOSOME ARE THE SAME AS THE GENES IN GENE_POSITION_DICT BY CREATING THE DICTIONARY FEATURE_POSITION_DICT CONTAINING ALL THE GENES IN FEATURE_ORF_DICT WITH THEIR CORRESPONDING POSITION IN THE CHROMOSOME
    _,_,gene_information_file=load_default_files()

    gene_alias_dict = gene_aliases(gene_information_file)[0]
    orf_position_dict = {}
    for feature in feature_orf_dict:
        if feature_orf_dict.get(feature)[5] == chrom:
            if feature in gene_position_dict:
                orf_position_dict[feature] = [feature_orf_dict.get(feature)[6], feature_orf_dict.get(feature)[7]]
            else:
                for feature_alias in gene_alias_dict.get(feature):
                    if feature_alias in gene_position_dict:
                        orf_position_dict[feature_alias] = [feature_orf_dict.get(feature)[6], feature_orf_dict.get(feature)[7]]



    if sorted(orf_position_dict) == sorted(gene_position_dict):
        if verbose == True:
            print('Everything alright, just ignore me!')
        
    else:
        print('WARNING: Genes in feature_list are not the same as the genes in the gene_position_dict. Please check!')

    
def build_dataframe(dna_dict,start_chr,end_chr,insrt_in_chrom_list,reads_in_chrom_list,genomicregions_list,chrom):
    """Main function that build the big dataframe with all genes characteristics 

    Parameters
    ----------
    dna_dict : dict
        1st output of the function intergenic_regions
    start_chr : int
        2nd output of the function gene_location
    end_chr : int
        3rd output of the function gene_location
    insrt_in_chrom_list : list
        1st output of the function read_wig_file
    reads_in_chrom_list : list
        2nd output of the function read_wig_file
    genomicregions_list : list
        All the annotated genomic regions, 2nd output of the intergenic_regions function
    chrom : str
        Name of the chromosome in roman where to extract the information.

    Returns
    -------
    dataframe
    - dna_df2: Dataframe containing information about the selected chromosome. This includes the following columns:
        - Feature name
        - Standard name of the feature
        - Aliases of feature name (if any)
        - Feature type (e.g. gene, telomere, centromere, etc. If None, this region is not defined)
        - Chromosome
        - Position of feature type in terms of bp relative to chromosome.
        - Length of region in terms of basepairs
        - Number of insertions in region
        - Number of insertions in truncated region where truncated region is the region without the first and last 100bp.
        - Number of reads in region
        - Number of reads in truncated region.
        - Number of reads per insertion (defined by Nreads/Ninsertions)
        - Number of reads per insertion in truncated region (defined by Nreads_truncatedgene/Ninsertions_truncatedgene)
        NOTE: truncated regions are only determined for genes. For the other regions the truncated region values are the same as the non-truncated region values.


        
    """

    _,essentials_file,gene_information_file=load_default_files()
    

    ## DETERMINE THE NUMBER OF TRANSPOSONS PER BP FOR EACH FEATURE

    reads_loc_list = [0] * len(dna_dict) # CONTAINS ALL READS JUST LIKE READS_IN_CHROM_LIST, BUT THIS LIST HAS THE SAME LENGTH AS THE NUMBER OF BP IN THE CHROMOSOME WHERE THE LOCATIONS WITH NO READS ARE FILLED WITH ZEROS
    i = 0
    
    for ins in insrt_in_chrom_list:
        if len(reads_loc_list) > ins-1: # there are some insertions outside  the chromosome that gives an error 
            reads_loc_list[ins-1] = reads_in_chrom_list[i]
            i += 1
    

    feature_NameAndType_list = []
    f_previous = dna_dict.get(start_chr)[0]
    f_type = dna_dict.get(start_chr)[1]
    N_reads = []
    N_reads_list_true=[]
    N_reads_list = []
    N_reads_truncatedgene_list = []
    N_insrt_truncatedgene_list = []
    N_insrt_list = []
    N_bp = 1
    N_bp_list = []
    f_start = 0
    f_end = 0
    f_pos_list = []
    i = 0
    for bp in dna_dict:
        f_current = dna_dict.get(bp)[0]
        if f_current == f_previous:
            f_type = dna_dict.get(bp)[1]
            f_end += 1
            N_bp += 1
            N_reads.append(reads_loc_list[i])
        elif (f_current != f_previous or (i+start_chr) == end_chr):# and not f_current.endswith('-A'):
            feature_NameAndType_list.append([f_previous, f_type])
            N_reads_list.append(sum(N_reads))
            N_reads_list_true.append(np.array(N_reads,dtype=float))
            N_insrt_list.append(len([ins for ins in N_reads if not ins == 0]))
            if not f_type == None and f_type.startswith('Gene'):
                N10percent = 100#int(len(N_reads) * 0.1) #TRUNCATED GENE DEFINITION
                N_reads_truncatedgene_list.append(sum(N_reads[N10percent:-N10percent]))
                N_insrt_truncatedgene_list.append(len([ins for ins in N_reads[N10percent:-N10percent] if not ins == 0]))
            else:
                N_reads_truncatedgene_list.append(sum(N_reads))
                N_insrt_truncatedgene_list.append(len([ins for ins in N_reads if not ins == 0]))

            N_bp_list.append(N_bp)
            N_reads = []
            N_bp = 1
            f_pos_list.append([f_start, f_end+f_start])
            f_start = f_start + f_end + 1
            f_end = 0
            f_previous = f_current
        i += 1

    N_reads_per_ins_list = []
    N_reads_per_ins_truncatedgene_list = []
    for i in range(len(N_reads_list)):
        if N_insrt_list[i] < 5: # upper bound of low number of transposons 
            N_reads_per_ins_list.append(0)
            N_reads_per_ins_truncatedgene_list.append(0)
        elif N_insrt_truncatedgene_list[i] < 5:
            N_reads_per_ins_list.append(N_reads_list[i]/(N_insrt_list[i]-1))
            N_reads_per_ins_truncatedgene_list.append(0)
        else:
            N_reads_per_ins_list.append(N_reads_list[i]/(N_insrt_list[i]-1))
            N_reads_per_ins_truncatedgene_list.append(N_reads_truncatedgene_list[i]/N_insrt_truncatedgene_list[i])


    #############get all essential genes together with their aliases##############
    with open(essentials_file, 'r') as f:
        essentials_temp_list = f.readlines()[1:]
    essentials_list = [essential.strip('\n') for essential in essentials_temp_list]
    del essentials_temp_list

    gene_alias_dict = gene_aliases(gene_information_file)[0]
    for key, val in gene_alias_dict.items():
        if key in essentials_list:
            for alias in val:
                essentials_list.append(alias)

    #ADD
    essentiality_list = []
    for feature in feature_NameAndType_list:
        if not feature[0] == "noncoding":
            if feature[1] in genomicregions_list:
                essentiality_list.append(None)
            elif feature[0] in essentials_list:
                essentiality_list.append(True)
            else:
                essentiality_list.append(False)
        else:
            essentiality_list.append(None)

    

    feature_name_list = []
    feature_type_list = []
    feature_alias_list = []
    feature_standardname_list = []
    for feature_name in feature_NameAndType_list:
        feature_name_list.append(feature_name[0])
        feature_type_list.append(feature_name[1])
        if feature_name[1] != None and feature_name[1].startswith('Gene') and feature_name[0] in gene_alias_dict:
            if gene_alias_dict.get(feature_name[0])[0] == feature_name[0]:
                feature_standardname_list.append(feature_name[0])
                feature_alias_list.append('')
            else:
                if len(gene_alias_dict.get(feature_name[0])) > 1:
                    feature_standardname_list.append(gene_alias_dict.get(feature_name[0])[0])
                    feature_alias_list.append(gene_alias_dict.get(feature_name[0])[1:])
                else:
                    feature_standardname_list.append(gene_alias_dict.get(feature_name[0])[0])
                    feature_alias_list.append('')
        else:
            feature_standardname_list.append(feature_name[0])
            feature_alias_list.append('')


    all_features = {'Feature_name': feature_name_list,
                    'Standard_name': feature_standardname_list,
                    'Feature_alias':feature_alias_list,
                    'Feature_type': feature_type_list,
                    'Essentiality': essentiality_list,
                    'Chromosome': [chrom]*len(feature_name_list),
                    'Position': f_pos_list,
                    'Nbasepairs':N_bp_list,
                    'Ninsertions':N_insrt_list,
                    'Ninsertions_truncatedgene':N_insrt_truncatedgene_list,
                    'Nreads':N_reads_list,
                    'Nreads_list':  N_reads_list_true,
                    'Nreads_truncatedgene':N_reads_truncatedgene_list,
                    'Nreadsperinsrt':N_reads_per_ins_list,
                    'Nreadsperinsrt_truncatedgene':N_reads_per_ins_truncatedgene_list}


    dna_df2 = pd.DataFrame(all_features, columns = [column_name for column_name in all_features]) #search for feature using: dna_df2.loc[dna_df2['Feature'] == 'CDC42']
    #CREATE NEW COLUMN WITH ALL DOMAINS OF THE GENE (IF PRESENT) AND ANOTHER COLUMN THAT INCLUDES LISTS OF THE BP POSITIONS OF THESE DOMAINS
    return dna_df2
