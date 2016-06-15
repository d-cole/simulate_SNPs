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

def get_reads_to_mut(reads):
    """Randomly chooses x unique reads to mutate, 
        where x is chosen from the binomial dist.

    Args:
        reads: List of read objects

    Returns:
        mut_reads: Random subset of reads of random size.
    """
    #Get number of reads to mutate
    num_reads = np.random.binomial(len(reads),p=0.5) 

    #Get num_reads random reads
    mut_reads = set() #Want num_read unique reads
    while len(mut_reads) < num_reads:
        mut_reads.add(reads[randint(0,len(reads) - 1)])

    return list(mut_reads)


def get_mut_strings(reads, base_pos, mutant_base):
    """Generates strings representing sites to mutate
    
    Args:
        reads: List of read objects to convert to mutant info strings
        base_pos: Position of base to mutate (relative to reference)
        mutant_base: New base to alter read.seq[pos relative to seq read]

    Returns:
        muts_str: List of strings of appropriate mutant info
        mut_str format: read_id\tbase_idx(relative to read)\told_bp\tnew_bp
    """
    muts_str = [] 

    for read in reads:
        mut_str = read.read_id + "\t" + str(read.direction) + "\t" + str(read.get_base_idx(base_pos)) + "\t" + \
             str(read.get_base_at_pos(base_pos)) + "\t" + mutant_base
        muts_str.append(mut_str)

    return muts_str


def get_reads(samtools_comm, direction):
    """
    """
    read_strs = check_output(samtools_comm, shell=True).split('\n')
    read_strs.remove("")
    reads = [read(y) for y in read_strs]
    [t_read.set_direction(direction) for t_read in reads]
    return reads 

    
if __name__ == "__main__":
    """
    Sample\tChrom\tbase_pos\n --> Sample\tChrom\tbase_pos\tRead_id\tRead_dir(1 or 2)\tbase_idx\told_base\tnew_base\n 

    For every site in file_in_loc, picks a random number of randomly chosen reads to mutate and writes their info to out_file.

    """
    file_in_loc = sys.argv[1]
    out_file_loc = sys.argv[2]

    out_file = open(out_file_loc,"w")

    with open(file_in_loc) as f:
        for line in f:
            print line
            #Sample\tChrom\tPOS\n
            sline = line.split()
            sample = sline[0]
            chrom = sline[1]
            pos = int(sline[2])

            #Get .bam path from sample name
            bam_path = glob.glob("/data/maggie.bartkowska/spirodela_ma/all_bam/realigned/*" + sample + "*.bam")[0]

            #samtools comm for getting reads at this site
            samtools_comm_fwd_reads = "samtools view " + bam_path + " " + \
                chrom + ":" + str(pos) + "-" + str(pos) + " -F 16"
            samtools_comm_rev_reads = "samtools view " + bam_path + " " + \
                chrom + ":" + str(pos) + "-" + str(pos) + " -f 16"

            reads = get_reads(samtools_comm_fwd_reads, direction = 1) \
                + get_reads(samtools_comm_rev_reads, direction = 2)

            bad_reads = []
            for t_read in reads:
                if not t_read.read_maps_pos(pos):
                    reads.remove(t_read)
                    bad_reads.append(t_read) 

            sys.stderr.write(line + "\n")
            for bad_read in bad_reads:
                sys.stderr.write(bad_read.raw_str + "\n")
                contains = str(bad_read in reads)
                sys.stderr.write(contains)
                
            
            #Randomly choose reads to mutate. Number to mutate chosen from binomial dist.
            reads_to_mutate = get_reads_to_mut(reads)
            print "Num reads to mutate", len(reads_to_mutate)

            #Pick random new base
            bases = ["A","T","C","G"]
            mutant_base = bases[randint(0, len(bases) - 1)]

            #Get strings for mutant reads
            mutant_strings = get_mut_strings(reads_to_mutate, pos, mutant_base)

            for mut_str in mutant_strings:
                complete_mut_str = line.strip("\n") + "\t" + mut_str + "\n"
                out_file.write(complete_mut_str)


    out_file.close()






    
