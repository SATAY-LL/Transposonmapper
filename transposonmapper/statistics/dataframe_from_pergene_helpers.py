import os
import numpy as np
import re 

def read_pergene_file(pergenefile):

    assert os.path.isfile(pergenefile), 'File not found at: %s' % pergenefile

    with open(pergenefile) as f:
        lines = f.readlines()[1:] #skip header

    genenames_list = [np.nan]*len(lines)
    tnpergene_list = [np.nan]*len(lines)
    readpergene_list = [np.nan]*len(lines) 

    line_counter = 0
    for line in lines:
        line_split = re.split(' |\t', line.strip('\n'))
        l = [x for x in line_split if x]

        if len(l) == 3:
            genenames_list[line_counter] = l[0]
            tnpergene_list[line_counter] = int(l[1])
            readpergene_list[line_counter] = int(l[2])

            line_counter += 1
    return genenames_list,tnpergene_list,readpergene_list,lines


def reads_per_insertion(tnpergene_list,readpergene_list,lines):

    readperinspergene_list = [np.nan]*len(lines)
    for i in range(len(tnpergene_list)):
        if not tnpergene_list[i] < 5:
            readperinspergene_list[i] = readpergene_list[i] / (tnpergene_list[i] -1)
        else:
            readperinspergene_list[i] = 0

    return readperinspergene_list