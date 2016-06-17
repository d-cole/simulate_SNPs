"""write_fake_mutants.py
Usage:
    python write_fake_mutants.py <output of get_read_ids.py> <.fqi file> <fq_fwd_file> <fq_rev_file>

"""
import sys

class read_mutate_info:
    def __init__(self, info_str):
        sline = info_str.split("\t")
        self.sample, self.chrom, self.pos, self.read_id, self.direction, self.base_idx, self.old_base, self.new_base  =  sline[0], \
            sline[1], sline[2], sline[3], sline[4], sline[5], sline[6], sline[7]


def load_read_dict(fqi_loc):
    """Loads fastq index file from provided location into dictionary mapping read id to byte location in .fq file.

    Args:
        fqi_loc: Location of .fqi file generated from indexFastq
    Returns:
        
    """
    id_to_byte = {}
    with open(fqi_loc) as f:
        for line in f:
            sline = line.split("\t")
            id_to_byte[sline[0]] = int(sline[1])

    return id_to_byte


def mutate_reads(fq_loc, fq_index, reads_to_mutate):
    """
    """
    fp = open(fq_loc, "rb") #need to change to 'r+b' for writing

    for read_mut in reads_to_mutate:
        byte_loc = fq_index[read_mut.read_id]

        # At start of read
        fp.seek(byte_loc)             
        # advance past the id
        fp.readline()
        fp.seek(int(read_mut.base_idx))
        #Should be at start of base sequence
        base = fp.read(1)
        print "found", base
        print "wanted", read_mut.old_base
        
    fp.close()


if __name__ == "__main__":
    reads_to_change = sys.argv[1]
    fq_index_loc = sys.argv[2]
    fq1_loc = sys.argv[3]
    #fq1_loc, fq2_loc = sys.argv[3], sys.argv[4]

    # Load dictionary of readID -> byte position
    fq_index_dict = load_read_dict(fq_index_loc)

    # Load reads to mutate
    reads_to_mutate = []
    with open(reads_to_change) as f:
        for line in f:
            reads_to_mutate.append(read_mutate_info(line))

      
    mutate_reads(fq1_loc, fq_index_dict, reads_to_mutate)
    
    


 


