import os
import numpy as np


def save_as_wig(wigfile, tncoordinates_array, ref_tid, readnumb_array):
    """This function writes in a .wig file located in the same folder as the bamfile, the information abot how many transposons
    were found in each genomic location. 

    Parameters
    ----------
    wigfile : str 
        Path with the filename extension included(e.g "data_file/wigfile_name.wig") describing where do you want to store the results.
        By default it will be stored in the same location as the bamfile, with the same basename. 
        Example, if the bamfile path is data_file/data_1.bam then the wig file will be data_file/data_1.bam.wig
    tncoordinates_array : numpy array 
        Second Output from the get_reads.py function : _,tncoordinates_array,_=get_reads(bam)
    ref_tid : dict 
        Output from the get_chromosome_names function : ref_tid = get_chromosome_names(bam)
    readnumb_array : numpy array 
        1st Output from the get_reads.py function : readnumb_array,_,_=get_reads(bam)
    """

    readnumbwig_array = readnumb_array
    ref_names = list(ref_tid.keys())

    unique_index_array = np.array([], dtype=int)  # =cc
    N_uniques_perchr_list = []
    ll = 0
    for kk in ref_names:
        # get indices for current chromosome.
        index = np.where(tncoordinates_array[:, 0] == int(ref_tid[kk] + 1))

        # get all insertion locations (in tncoordinates, all rows, column 1)
        unique_index = np.unique(tncoordinates_array[index][:, 1], return_index=True)[1]

        unique_index_array = np.append(unique_index_array, (unique_index + ll), axis=0)

        # total amount unique indices found untill current chromosome
        ll += np.count_nonzero(tncoordinates_array[:, 0] == int(ref_tid[kk] + 1))
        N_uniques_perchr_list.append(ll)

    # Collect duplicates
    duplicate_list = []  # =dd
    ll = 0
    index_last_unique_previous_chromosome = 0
    for ii in N_uniques_perchr_list:
        index_last_unique = np.where(unique_index_array <= ii)[0][-1]
        for jj in range(ll, ii):
            if (
                int(jj)
                not in unique_index_array[
                    index_last_unique_previous_chromosome:index_last_unique
                ]
            ):
                duplicate_list.append(jj)
        index_last_unique_previous_chromosome = index_last_unique
        ll = ii

    # SUM READNUMB VALUES AT INDEX IN DUPLICATE_LIST AND DUPLICATE_LIST-1
    for ii in duplicate_list:
        readnumbwig_array[ii - 1] = readnumbwig_array[ii - 1] + readnumbwig_array[ii]

    tncoordinateswig_duplicatesremoved_array = np.delete(
        tncoordinates_array, duplicate_list, axis=0
    )
    readnumbwig_duplicatesremoved_array = np.delete(
        readnumbwig_array, duplicate_list, axis=0
    )

    # Write wigfile
    with open(wigfile, "w") as f:
        base = os.path.basename(wigfile)
        filename = os.path.splitext(base)[0]
        f.write("track type=wiggle_0 ,maxheightPixels=60 name=" + filename + "\n")
        for kk in ref_names:
            f.write("VariableStep chrom=chr" + kk + "\n")

            index = np.where(
                tncoordinateswig_duplicatesremoved_array[:, 0] == int(ref_tid[kk] + 1)
            )  # get indices for current chromosome.
            for ii in index[0]:
                f.write(
                    str(tncoordinateswig_duplicatesremoved_array[ii][1])
                    + " "
                    + str(readnumbwig_duplicatesremoved_array[ii])
                    + "\n"
                )
