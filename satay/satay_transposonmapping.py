import sys
from transposonmapper import transposonmapper

bam_arg = sys.argv[1]


def satay_transposonmapping(bamfile=bam_arg):
    transposonmapper(bamfile=bamfile)


if __name__ == "__main__":
    satay_transposonmapping()

