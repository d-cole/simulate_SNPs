"""
Usage:
    python get_read_ids.py <sites file from get_rand_sites.py> <out_file>

"""
import sys
import glob
from subprocess import call
from subprocess import check_output
from read import read
import numpy as np
from random import randint

def get_reads_to_mut(read_list):
    """Randomly chooses x unique reads to mutate, 
        where x is chosen from the binomial dist.

    Args:
        reads: List of read objects

    Returns:
        mut_reads: Random subset of reads of random size.
    """
    #Get number of reads to mutate
    num_reads = np.random.binomial(len(read_list),p=0.5) 

    #Get num_reads random reads
    mut_reads = set() #Want num_read unique reads
    while len(mut_reads) < num_reads:
        mut_reads.add(read_list[randint(0,len(read_list) - 1)])

    return list(mut_reads)


def get_mut_strings(reads, base_pos, mutant_base):
    """Generates strings representing sites to mutate
    
    Args:
        reads: List of read objects to convert to mutant info strings
        base_pos: Position of base to mutate (relative to reference)
        mutant_base: New base to alter read.seq[pos relative to seq read]

    Returns:
        muts_str: List of strings of appropriate mutant info
    """
    base_comp = {"A":"T", "C":"G", "G":"C", "T":"A", "a":"t", "t":"a", "g":"c", "c":"g"}

    muts_str = [] 
    for read in reads:
        curr_mutant_base = mutant_base

        if read.rev_comp:
            curr_mutant_base = base_comp[mutant_base]

        mut_str = read.read_id[13:] + "\t" + str(read.rev_comp) + "\t" + str(read.get_base_idx(base_pos)) + "\t" + \
            str(read.get_base_at_pos(base_pos)) + "\t" + curr_mutant_base + "\t" + read.seq

        muts_str.append(mut_str)

    return muts_str


def get_reads(samtools_comm, rev_comp):
    """
    """
    read_strs = check_output(samtools_comm, shell=True).split('\n')
    read_strs.remove("")
    reads = [read(y) for y in read_strs]
    [t_read.set_rev_comp(rev_comp) for t_read in reads]

    return reads 

    
if __name__ == "__main__":
    """
    Sample\tChrom\tbase_pos\n -->
    Sample\tChrom\tbase_pos\tRead_id\treverse complement? (0 or 1)\tbase_idx
    \told_base (if reverse complement this base will be the complement of reference base)
    \tnew_base(if rev comp this base will be the complement of other reads in this sample)
    \tsequence string\n

    For every site in file_in_loc, picks a random number of randomly chosen reads to mutate and writes their info to out_file.

    """
    file_in_loc = sys.argv[1]
    out_file_loc = sys.argv[2]

    out_file = open(out_file_loc,"w")

    with open(file_in_loc) as f:
        for line in f:
            #print line
            #Sample\tChrom\tPOS\n
            sline = line.split()
            sample = sline[0]
            chrom = sline[1]
            pos = int(sline[2])

            #Get .bam path from sample name
            bam_path = glob.glob("/data/maggie.bartkowska/spirodela_ma/all_bam/realigned/*" + sample + "*.bam")[0]

            #samtools comm for getting reads at this site
            samtools_comm_fwd = "samtools view " + bam_path + " " + \
                chrom + ":" + str(pos) + "-" + str(pos) + " -F 16"

            samtools_comm_rev_comp = "samtools view " + bam_path + " " + \
                chrom + ":" + str(pos) + "-" + str(pos) + " -f 16"

            reads = get_reads(samtools_comm_fwd, rev_comp = 0) \
                + get_reads(samtools_comm_rev_comp, rev_comp = 1)

            good_reads = []
            for t_read in reads:
                if t_read.read_maps_pos(pos):
                    good_reads.append(t_read)

            #Randomly choose reads to mutate. Number to mutate chosen from binomial dist.
            reads_to_mutate = get_reads_to_mut(good_reads)
            
            #Pick random new base
            bases = ["A","T","C","G"]
            mutant_base = bases[randint(0, len(bases) - 1)]

            #Get strings for mutant reads
            mutant_strings = get_mut_strings(reads_to_mutate, pos, mutant_base)

            for mut_str in mutant_strings:
                complete_mut_str = line.strip("\n") + "\t" + mut_str + "\n"
                out_file.write(complete_mut_str)


    out_file.close()






    
