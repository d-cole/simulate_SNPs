#include <stdio.h>
#include <stdlib.h>

#define SEQ_BYTES 259
#define ID_LEN 55
// 55 (header line), 100 (seq), 1 ('+'), 100 (base qual), 3 (3 x '\n')
// Not sure if header line will be constant across all samples
// @DD63XKN1:432:C7RRYACXX:1:1101:1145:1061 1:N:0:GCCAATA
// @DD63XKN1: instrument ID
// 432: run number on instrument
// C7RRYACXX: flowcell ID
// 1: line number
// 1101: tile number
// 1145: X coord of cluster
// 1061 Y coord of cluster
// 1: Read number 1
// N: Is the read filtered (No)
// 0: Control number
// GCCAATA Index sequence

// Use flowcellID:LineNumber:tileNumber:Xcoord:Ycoord as unique read IDs

char ** get_seq_id(FILE *fp){
    /*
    *
    */
    char *seq_id = (char *)malloc((sizeof(char) * ID_LEN + 1));
    fread(seq_id, 1, ID_LEN, fp);
    seq_id[ID_LEN] = '\0';

    return seq_id;
}

int main(int argc, char **argv){

    char *fastq_in = argv[1];

    FILE *fp;
    fp = fopen(fastq_in, "r");

            









}



