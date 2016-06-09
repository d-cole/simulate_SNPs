import sys
import glob
from subprocess import call

if __name__ == "__main__":

    file_in_loc = sys.argv[1]
    out_file_loc = sys.argv[2]

    out_file = open(out_file_loc,"w")

    with open(file_in_loc) as f:
        for line in f:
            #Sample\tChrom\tPOS\n
            sline = line.split()
            glob_str = glob.glob("/data/maggie.bartkowska/spirodela_ma/all_bam/realigned/*" + sline[0] + "*.bam")[0]

            samtools_comm = "samtools view " + glob_str + " " + \
                sline[1] + ":" + sline[2] + "-" + sline[2]
            call(samtools_comm, shell=True)

    out_file.close()






    
