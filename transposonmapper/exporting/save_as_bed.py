import os


def save_as_bed(file, tncoordinates_array, ref_tid, readnumb_array):
    """This function writes in a .bed file located in the same folder as the bamfile, the information abot how many transposons
    were found in each genomic location. 

    Parameters
    ----------
    file : str
        Path with the filename extension included(e.g "data_file/bedfile_name.bed") describing where do you want to store the results.
        By default it will be stored in the same location as the bamfile, with the same basename. 
        Example, if the bamfile path is data_file/data_1.bam then the bed file will be data_file/data_1.bam.bed 
    tncoordinates_array : numpy array 
        Second Output from the get_reads.py function : _,tncoordinates_array,_=get_reads(bam)
    ref_tid : dict 
        Output from the get_chromosome_names function : ref_tid = get_chromosome_names(bam)
    readnumb_array : numpy array 
        1st Output from the get_reads.py function : readnumb_array,_,_=get_reads(bam)
    """

    with open(file, "w") as f:

        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]
        f.write("track name=" + filename + " useScore=1\n")

        coordinates_counter = 0
        for tn in tncoordinates_array:
            refname = [key for key, val in ref_tid.items() if val == tn[0] - 1][0]
            if refname == "Mito":
                refname = "M"
            f.write(
                "chr"
                + refname
                + " "
                + str(tn[1])
                + " "
                + str(tn[1] + 1)
                + " . "
                + str(100 + readnumb_array[coordinates_counter] * 20)
                + "\n"
            )
            coordinates_counter += 1
