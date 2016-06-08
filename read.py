"""
read.py

Class representing a single sequence read in the .sam format.
"""

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
        self.pos = sline[3]
        self.MAPQ = sline[4]
        self.CIGAR = sline[5]
        self.mate_chrom = sline[6]
        self.mate_pos = sline[7]
        self.template_len = sline[8]
        self.seq = sline[9]
        self.base_qual = sline[1]
        ##Flags & duplicates?

        if len(seq) != int(template_len):
            pass
        
#        self.base_range = range(int(self.pos), int(self.pos) + len(self.template_len))
        self.range_end = int(self.pos) + len(self.template_len)
     
    
    def get_base_at_pos(self, pos):
        """
        *Check tensorflow documentation
        *throw exception
        """
        if not (self.pos <= pos <= self.range_end):
            #Raise exception & return
            pass
        #! 1 or 0 base of pos and seq array
        pass
        
        
            







