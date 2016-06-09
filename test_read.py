from read import read




if __name__ == "__main__":
    reads = []

    with open("example_reads.txt", "r") as read_f:
        for line in read_f:
            reads.append(read(line))                               

   
    pos = 100
    for read in reads:
        print read.get_base_at_pos(pos),"  " , read.get_base_qual_at_pos(pos), "   ", read.MAPQ
    
