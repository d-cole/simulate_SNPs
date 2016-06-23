"""write_fake_mutants.py
Usage:
    python write_fake_mutants.py <output of get_read_ids.py> <.fq1 file> <fqi1 file> <.fq2 file> <.fqi2 file>

"""
import sys

class read_mutate_info:
    #Need to adjust to add sequence info
    def __init__(self, info_str):
        sline = info_str.split("\t")
        self.raw_str = info_str
        self.sample, self.chrom, self.pos, self.read_id, self.rev_comp, self.base_idx, self.old_base, self.new_base, self.seq  =  sline[0], \
            sline[1], sline[2], sline[3], sline[4], int(sline[5]), sline[6], sline[7], sline[8]


def load_read_dict(fqi_loc, target_dict):
    """Loads fastq index file from provided location into dictionary mapping read id to byte location in .fq file.

    Args:
        fqi_loc: Location of .fqi file generated from indexFastq
        
    """
    with open(fqi_loc) as f:
        for line in f:
            sline = line.split("\t")
            if target_dict.get(sline[0], None) == None:
                target_dict[sline[0]] = [int(sline[1])]

            else:
                #Fq1 byte offsets already added
                target_dict[sline[0]].append(int(sline[1]))

    return


def mutate_reads(fq_loc, fq_index, reads_to_mutate):
    """
    """
    fp = open(fq_loc, "rb") #need to change to 'r+b' for writing

    for read_mut in reads_to_mutate:
        byte_loc = fq_index[read_mut.read_id]

        # At start of read
        fp.seek(byte_loc)             
        # advance past the id
        id_line = fp.readline()
        start_pos = fp.tell()
        fp.seek(int(read_mut.base_idx),1)
        #Should be at start of base sequence
        base = fp.read(1)
#        print id_line
#        print "found", base
#        print "pos", read_mut.pos
#        print "base_idx", read_mut.base_idx
#        print "wanted", read_mut.old_base

        print "--------------------START-------------------"
        fp.seek(byte_loc)
        entry_str = fp.readline() + fp.readline() + fp.readline() + fp.readline()
        fp.seek(start_pos)
        print "At start", fp.read(5)
        print "ENTRY", entry_str
        print "found", base
        print "wanted", read_mut.old_base 
        print "found id: ", id_line
        print read_mut.raw_str

        if base != read_mut.old_base:
            print "mismatch"
            fp.seek(byte_loc)
            fp.readline()
            fp.seek(read_mut.base_idx -1,1)
            print "pos n-1", fp.read(3)
        else:
            print "match"
            fp.seek(byte_loc)
            fp.readline()
            fp.seek(read_mut.base_idx - 1, 1)
            print "pos n-1", fp.read(3)
        
            

        print "--------------------END------------------------"
       
        
    fp.close()


if __name__ == "__main__":
    reads_to_change = sys.argv[1]
    fq1_loc, i_fq1_loc, fq2_loc, i_fq2_loc = sys.argv[2], sys.argv[3],\
         sys.argv[4], sys.argv[5]

    read_index = {}

    # Load dictionary of readID -> byte position
    load_read_dict(i_fq1_loc, read_index)
    load_read_dict(i_fq2_loc, read_index)

    # Load reads to mutate
    reads_to_mutate = []
    with open(reads_to_change) as f:
        for line in f:
            reads_to_mutate.append(read_mutate_info(line))


    fp1 = open(fq1_loc, "rb") #need to change to 'r+b' for writing
    fp2 = open(fq2_loc, "rb")

    for read_mut in reads_to_mutate:
        f1_byte_loc = read_index[read_mut.read_id][0]
        f2_byte_loc = read_index[read_mut.read_id][1]

        #move fp to start of entry with matching read id
        fp1.seek(f1_byte_loc)
        fp2.seek(f2_byte_loc)

        #Get the read ids/seek over varying length id line
        fp1_id = fp1.readline()
        fp2_id = fp2.readline()
        
        #Get position at start of sequence string 
        fp1_seq_pos = fp1.tell()
        fp2_seq_pos = fp2.tell()

        #Get sequence strings
        fp1_seq = fp1.readline()
        fp2_seq = fp2.readline()

        #Determine if read came from fq1 or fq2
        if read_mut.seq == fp1_seq:
            focal_fp = fp1
            focal_fp.seek(fp1_seq_pos)

        elif read_mut.seq == fp2_seq:
            focal_fp = fp2 
            focal_fp.seek(fp2_seq_pos) 
        else:
            raise ValueError("No sequence match in fq1 or fq2") 

        focal_fp.seek(int(read_mut.base_idx),1)
        base = focal_fp.read(1)

        if base != read_mut.old_base:
            print "mismatch"
            print "Expected", read_mut.old_base
            print "Found", base

        else:
            print "match"



    fp1.close()
    fp2.close()

#        # At start of read
#        fp.seek(byte_loc)             
#        # advance past the id
#        id_line = fp.readline()
#        start_pos = fp.tell()
#        fp.seek(int(read_mut.base_idx),1)
#        #Should be at start of base sequence
#        base = fp.read(1)
##        print id_line
##        print "found", base
##        print "pos", read_mut.pos
##        print "base_idx", read_mut.base_idx
##        print "wanted", read_mut.old_base
#
#        print "--------------------START-------------------"
#        fp.seek(byte_loc)
#        entry_str = fp.readline() + fp.readline() + fp.readline() + fp.readline()
#        fp.seek(start_pos)
#        print "At start", fp.read(5)
#        print "ENTRY", entry_str
#        print "found", base
#        print "wanted", read_mut.old_base 
#        print "found id: ", id_line
#        print read_mut.raw_str
#
#        if base != read_mut.old_base:
#            print "mismatch"
#            fp.seek(byte_loc)
#            fp.readline()
#            fp.seek(read_mut.base_idx -1,1)
#            print "pos n-1", fp.read(3)
#        else:
#            print "match"
#            fp.seek(byte_loc)
#            fp.readline()
#            fp.seek(read_mut.base_idx - 1, 1)
#            print "pos n-1", fp.read(3)
#        
#            
#
#        print "--------------------END------------------------"
#       
        


 


