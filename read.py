"""
read.py

Class representing a single sequence read in the .sam format.
"""
import sys
#DD63XKN1:432:C7RRYACXX:1:1307:18100:35594       113     pseudo1 7       1       5M1D7M1D88M     pseudo2 8795984 0       CTCAACCCTAAACCCTAAACCCTAAACCCTAAACCCTAAACCCTAAGCCCTAAACCCTAAACCCTAAACCCTAAACCCTGGGCTGCTCATTTGCAGGAAA    B7'07BB<<7<7FFFFBBBBBBB<70BBBBB<'FFB<<B<FF<FFBBFFBBFBBFFFF<B<IFFFFBBIIFFFF<IIIIFIIIIIFIFFFBFFFFFF<BB    PG:Z:MarkDuplicates     RG:Z:1  NM:i:2  SM:i:67 MQ:i:0  PQ:i:237        UQ:i:90 XQ:i:22

class read():
    
    def __init__(self,read_str):
        """
        """
        self.raw_str = read_str
        sline = read_str.split('\t')
        self.read_id = sline[0]
        self.flag = sline[1]
        self.chrom = sline[2]
        self.read_start = int(sline[3])
        self.MAPQ = sline[4]
        self.CIGAR = sline[5]
        self.mate_chrom = sline[6]
        self.mate_pos = sline[7]
        self.template_len = sline[8]
        self.seq = sline[9]
        self.base_qual = sline[10]
        self.direction = None

        if len(self.seq) != 100:
            print "Seq len:", len(self.seq), "\n", "Temp len:", self.template_len, \
                "MQ: ", self.MAPQ
    
#        self.base_range = range(int(self.read_start), int(self.read_start) + len(self.template_len))
        self.range_end = self.read_start + (len(self.seq) - 1)

    def set_direction(self, direction):
        """
        """
        self.direction = direction

    def get_base_idx(self, pos):
        """

        """    
        idx = int(pos) - self.read_start

        # Reverse strand
        if idx < 0:
            idx = len(self.seq) + idx

        return idx

    def read_maps_pos(self, pos):
#        print "read maps", self.read_start, pos, self.range_end
#        print self.raw_str
        return ((self.read_start <= int(pos)) and (int(pos) <= self.range_end))

 
    def get_base_at_pos(self, pos):
        """Gets base pair at given position.

        Args:
            pos: Integer bp position on a chromosome

        Returns:
            Single character representing base pair

        Raises:
            ValueError if specified position is not covered by this read
        """
        if not ((self.read_start <= pos) and (pos <= self.range_end)):
            sys.stderr.write("Err\n")
            sys.stderr.write(self.raw_str  +"\n")
            sys.stderr.write(str(self.read_start) + " " + str(pos) + " " + str(self.range_end) + "\n")

            raise ValueError("Read does not cover specified position")

        base_idx = self.get_base_idx(pos)
        try:
            base = self.seq[base_idx]
        except:
            print "Base index fail"
            print "target pos", pos
            print "Start pos", self.read_start
            print self.raw_str
            print base_idx
            print len(self.seq)

        return self.seq[base_idx]


    def get_base_qual_at_pos(self, pos):
       """Gets base pair quality of a base at given position.

       Args:
           pos: Integer bp position on a chromosome

       Returns:
           Int representing base pair quality. ord(base_str) - 33

       Raises:
           ValueError if specified position is not covered by this read
       """
       if not ((self.read_start <= pos) and (pos <= self.range_end)):
           print self.read_start
           print pos
           print self.range_end
           raise ValueError("Read does not cover specified position")

       base_idx = self.get_base_idx(pos)
       return ord(self.base_qual[base_idx]) - 33

  
           







