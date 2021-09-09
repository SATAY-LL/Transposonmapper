def save_per_gene(filename, tn_per_gene, reads_per_gene, aliases_designation):
    """Create text file with transposons and reads per gene
 
    NOTE THAT THE TRANSPOSON WITH THE HIGHEST READ COUNT IS IGNORED.
    E.G. IF THIS FILE IS COMPARED WITH THE _PERGENE_INSERTIONS.TXT FILE THE 
    READS DON'T ADD UP (SEE https://groups.google.com/forum/#!category-topic/satayusers/bioinformatics/uaTpKsmgU6Q)
    TOO REMOVE THIS HACK, CHANGE THE INITIALIZATION OF THE VARIABLE readpergene

    Parameters
    ----------
    filename : str
        Path with the filename extension included(e.g "data_file/file.txt") 
        describing where do you want to store the results.
        By default it will be stored in the same location as the bamfile, 
        with the same basename. 
        Example, if the bamfile path is data_file/data_1.bam then the  file will be data_file/data_1.bam_pergene.txt
    tn_per_gene : int 
        The number of transposons found per gene 
    reads_per_gene : int
        The number of reads found per gene 
    aliases_designation : dict
        Last output of the function read_genes  _, _, aliases_designation = read_genes(
        gff_file, essential_file, gene_name_file)
    """

    with open(filename, "w") as f:

        f.write("Gene name\tNumber of transposons per gene\tNumber of reads per gene\n")

        for gene in tn_per_gene:
            tnpergene = tn_per_gene[gene]
            readpergene = reads_per_gene[gene]
            if gene in aliases_designation:
                gene_alias = aliases_designation.get(gene)[0]
            else:
                gene_alias = gene
            f.write(gene_alias + "\t" + str(tnpergene) + "\t" + str(readpergene) + "\n")

