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
        mut_str = read.read_id + "\t" + str(read.get_base_idx(base_pos)) + "\t" + \
             str(read.get_base_at_pos(base_pos)) + "\t" + mutant_base
        muts_str.append(mut_str)

    return muts_str

    
if __name__ == "__main__":
    """
    Sample\tChrom\tbase_pos\n --> Sample\tChrom\tbase_pos\tRead_id\tbase_idx\told_base\tnew_base\n 

    For every site in file_in_loc, picks a random number of randomly chosen reads to mutate and writes their info to out_file.

    """
    file_in_loc = sys.argv[1]
    out_file_loc = sys.argv[2]

    out_file = open(out_file_loc,"w")

    with open(file_in_loc) as f:
        for line in f:
            #Sample\tChrom\tPOS\n
            sline = line.split()
            sample = sline[0]
            chrom = sline[1]
            pos = sline[2]

            #Get .bam path
            glob_str = glob.glob("/data/maggie.bartkowska/spirodela_ma/all_bam/realigned/*" + sample + "*.bam")[0]

            #samtools comm for getting reads at this site
            samtools_comm = "samtools view " + glob_str + " " + \
                chrom + ":" + pos + "-" + pos

            #Get reads covering specified site using samtools view
            read_strs = check_output(samtools_comm, shell=True).split('\n')
            #Remove null string "" from after final'\n'
            read_strs.remove("")

            #Convert to sam lines to read objects
            reads = [read(y) for y in read_strs]

            bad_reads = []
            for t_read in reads:
                if not t_read.read_maps_pos(pos):
                    reads.remove(t_read)
                    bad_reads.append(t_read) 

            print bad_reads
            print reads

            #Randomly choose reads to mutate. Number to mutate chosen from binomial dist.
            reads_to_mutate = get_reads_to_mut(reads)
        
            #print len(reads_to_mutate)
            #Pick random new base
            bases = ["A","T","C","G"]
            mutant_base = bases[randint(0, len(bases) - 1)]

            #Get strings for mutant reads
            mutant_strings = get_mut_strings(reads_to_mutate, pos, mutant_base)

            for mut_str in mutant_strings:
                complete_mut_str = line.strip("\n") + "\t" + mut_str + "\n"
                out_file.write(complete_mut_str)


    out_file.close()






    
