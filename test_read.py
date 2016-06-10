from read import read
import sys



if __name__ == "__main__":
    reads = []

    with open(sys.argv[1], "r") as read_f:
        for line in read_f:
            reads.append(read(line))                               
   
    pos = 8878
    bases = {}
    for read in reads:
        base = read.get_base_at_pos(pos)



        bases[base] = bases.get(base,0)
        bases[base] += 1

        print read.get_base_at_pos(pos),"  " , read.get_base_qual_at_pos(pos), "   ", read.MAPQ

    print bases    
    
