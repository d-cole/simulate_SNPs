"""
Usage:
    python get_rand_sites.py <num_sites> <out_file>

"""
import sys
from random import randint

if __name__ == "__main__":

    num_random = int(sys.argv[1])
    out_file_loc = sys.argv[2]

    #Load chromosome size info from .fai
    chrom_sizes = {}

    samples = ["CC_A","CC_B","CC_C","CC_D","CC_E","CC_F","CC_H","CC_I","CC_J","CC_K",\
        "CC_L","CC_N","CC_O","CC_P","GP2-3_A","GP2-3_B","GP2-3_C","GP2-3_D",\
        "GP2-3_E","GP2-3_F","GP2-3_G","GP2-3_H","GP2-3_I","GP2-3_J","GP2-3_K",\
        "GP2-3_L","GP2-3_M","GP2-3_N","GP2-3_O","GP2-3_P"]

    #Load chromosome sizes
    with open("altered_pseudo_plastids.fai", "r") as f:
        for line in f:
            sline = line.split("\t")
            chrom_sizes[sline[0]] = int(sline[1])

    #Remove chromosomes excluded from analysis
    chrom_sizes.pop("pseudo0", None)
    chrom_sizes.pop("mitochondrion", None)
    chrom_sizes.pop("chloroplast", None)

    #Write out random sample, chrom and pos to out_file
    out_file = open(out_file_loc,"w")
    chroms = chrom_sizes.keys()

    for i in range(0, num_random):
        rand_sample = samples[randint(0,len(samples) - 1)] 
        rand_chrom = chroms[randint(0,len(chroms) - 1)]
        rand_pos = randint(0,chrom_sizes[rand_chrom])

        out_str = rand_sample + '\t' + rand_chrom + '\t' + str(rand_pos) + '\n'
        out_file.write(out_str)


    out_file.close()






    
