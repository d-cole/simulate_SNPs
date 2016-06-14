/*indexFastq creates a file of the format <read id>\t<byte offset> for every read in a given .fastq file
* The Fastq Index file will be ~11% of the size of the given .fastq file.
*
* Example id:  @DD63XKN1:432:C7RRYACXX:1:1101:1145:1061 1:N:0:GCCAATA
* Truncated id: C7RRYACXX:1:1101:1145:1061 
*/
#include <stdio.h>
#include <stdlib.h>

#define ENTRY_BYTES 259
#define ID_LEN 27
#define _FILE_OFFSET_BITS 64

int main(int argc, char **argv){
    char *fastq_in = argv[1];
    char *fastq_index_out = argv[2];

    FILE *in_fp, *out_fp;
    in_fp = fopen(fastq_in, "r");
    out_fp = fopen(fastq_index_out, "w+"); 
 
    char seq_id[ID_LEN + 1];
    off_t entry_pos = 0;

    //Skip first 14 bits of all ids
    fseek(in_fp, 14, SEEK_CUR);

    while(!feof(in_fp) && (fread(seq_id, ID_LEN, 1, in_fp) == 1)){
        seq_id[ID_LEN] = '\0';
    
        //Multiple writing 
        fprintf(out_fp,"%s\t%lld\n", seq_id, entry_pos);

        //Adjust file pointer to next entry
        //Already ID_LEN bytes intro current entry
        fseek(in_fp, ENTRY_BYTES - ID_LEN, SEEK_CUR);
        entry_pos += ENTRY_BYTES;
    }

    fclose(in_fp);
    fclose(out_fp);
}

