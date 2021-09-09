def save_per_gene_insertions(
    filename,
    tn_coordinates,
    gene_coordinates,
    chr_lengths_cumsum,
    ref_tid_roman,
    aliases_designation,
):
    """This function write in txt file 5 columns of information about transposon insertions separated by tabs. 
    The tabs are: Gene name,Chromosome,Start location,End location,Insertion locations,Reads per insertion location

    Parameters
    ----------
    filename : str
        Path with the filename extension included(e.g "data_file/file.txt") describing where do you want to store the results.
        By default it will be stored in the same location as the bamfile, with the same basename. 
        Example, if the bamfile path is data_file/data_1.bam then the per_gene file will be data_file/data_1.bam_pergene_insertions.txt
    tn_coordinates : dict
         Last output of the function get_insertions _,_, tn_coordinates_per_gene = get_insertions_and_reads(
        gene_coordinates, tncoordinatescopy_array, readnumb_array)
    gene_coordinates : dict 
        Output of the function add_chromosome_length:  gene_coordinates = add_chromosome_length(
        gene_coordinates, chr_lengths_cumsum, ref_tid_roman)
    chr_lengths_cumsum : dict
        last output of the function get_sequence_length : _, chr_lengths_cumsum = get_sequence_length(bam)
    ref_tid_roman : dict 
        Dictionary describing roman names as keys , 
        ref_romannums = chromosomename_roman_to_arabic()[1]
        ref_tid_roman = {key: value for key, value in zip(ref_romannums, ref_tid)}
    aliases_designation : dict
        Last output of the function read_genes  _, _, aliases_designation = read_genes(
        gff_file, essential_file, gene_name_file)
    """

    with open(filename, "w") as f:

        f.write(
            "Gene name\tChromosome\tStart location\tEnd location\tInsertion locations\tReads per insertion location\n"
        )

        for gene in tn_coordinates:
            gene_chrom = ref_tid_roman.get(gene_coordinates.get(gene)[0])
            tncoordinates = [
                ins - chr_lengths_cumsum.get(gene_chrom)
                for ins in tn_coordinates[gene][3]
            ]

            if gene in aliases_designation:
                gene_alias = aliases_designation.get(gene)[0]
            else:
                gene_alias = gene

            f.write(
                gene_alias
                + "\t"
                + str(tn_coordinates[gene][0])
                + "\t"
                + str(tn_coordinates[gene][1] - chr_lengths_cumsum.get(gene_chrom))
                + "\t"
                + str(tn_coordinates[gene][2] - chr_lengths_cumsum.get(gene_chrom))
                + "\t"
                + str(tncoordinates)
                + "\t"
                + str(tn_coordinates[gene][4])
                + "\n"
            )


def save_per_essential_insertions(
    filename,
    tn_coordinates,
    gene_coordinates,
    chr_lengths_cumsum,
    ref_tid_roman,
    aliases_designation,
):
    """This function generates a .txt file with the insertions in the annotated 
    essential genes in WT. 

    Parameters
    ----------
    filename : str
        Path with the filename extension included(e.g "data_file/file.txt") 
        describing where do you want to store the results.
        By default it will be stored in the same location as the bamfile, 
        with the same basename. 
        Example, if the bamfile path is data_file/data_1.bam then the  file will be data_file/data_1.bam_peressential_insertions.txt
    tn_coordinates : dict
         Last output of the function get_insertions _,_, tn_coordinates_per_gene = get_insertions_and_reads(
        gene_coordinates, tncoordinatescopy_array, readnumb_array)
    gene_coordinates : dict 
        Output of the function add_chromosome_length:  gene_coordinates = add_chromosome_length(
        gene_coordinates, chr_lengths_cumsum, ref_tid_roman)
    chr_lengths_cumsum : dict
        last output of the function get_sequence_length : _, chr_lengths_cumsum = get_sequence_length(bam)
    ref_tid_roman : dict 
        Dictionary describing roman names as keys , 
        ref_romannums = chromosomename_roman_to_arabic()[1]
        ref_tid_roman = {key: value for key, value in zip(ref_romannums, ref_tid)}
    aliases_designation : dict
        Last output of the function read_genes  _, _, aliases_designation = read_genes(
        gff_file, essential_file, gene_name_file)
    """

    with open(filename, "w") as f:

        f.write(
            "Essential gene name\tChromosome\tStart location\tEnd location\tInsertion locations\tReads per insertion location\n"
        )

        for gene in tn_coordinates:
            gene_chrom = ref_tid_roman.get(gene_coordinates.get(gene)[0])
            tncoordinates = [
                ins - chr_lengths_cumsum.get(gene_chrom)
                for ins in tn_coordinates[gene][3]
            ]

            if gene in aliases_designation:
                gene_alias = aliases_designation.get(gene)[0]
            else:
                gene_alias = gene

            f.write(
                gene_alias
                + "\t"
                + str(tn_coordinates[gene][0])
                + "\t"
                + str(tn_coordinates[gene][1] - chr_lengths_cumsum.get(gene_chrom))
                + "\t"
                + str(tn_coordinates[gene][2] - chr_lengths_cumsum.get(gene_chrom))
                + "\t"
                + str(tncoordinates)
                + "\t"
                + str(tn_coordinates[gene][4])
                + "\n"
            )
