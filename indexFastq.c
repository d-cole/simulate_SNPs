/*indexFastq creates a file of the format <read id>\t<byte offset> for every read in a given .fastq file
* The Fastq Index file will be ~11% of the size of the given .fastq file.
*
* Example id:  @DD63XKN1:432:C7RRYACXX:1:1101:1145:1061 1:N:0:GCCAATA
* Truncated id: C7RRYACXX:1:1101:1145:1061 
*/
#include <stdio.h>
#include <stdlib.h>

#define ENTRY_NO_READID_BYTES 204 //101('seq\n') + 2 ('+\n') + 101('qual\n')
#define _FILE_OFFSET_BITS 64
#define ID_BUFFER_SIZE 100
#define TRUNC_HEAD_SIZE 14

int get_id_len(char *seq_id, int buff_size){
    int i;
    for(i = 0; i < buff_size; i++){
        if (seq_id[i] == '\n'){
            return i + 1;     
        }
    }

    return -1;
}


void truncate_seq_id(char **seq_id, int buff_size){
    /* Removes unnecessary info from tail and head of the id string*/

    //Remove head of id 
    *seq_id += TRUNC_HEAD_SIZE;

    //Remove tail end of id
    int i;
    for(i = 0; i < buff_size; i++){
        if ((*seq_id)[i] == ' '){
            (*seq_id)[i] = '\0';
            return;
        }
    } 
}


int main(int argc, char **argv){
    char *fastq_in = argv[1];
    char *fastq_index_out = argv[2];

    FILE *in_fp, *out_fp;
    in_fp = fopen(fastq_in, "r");
    out_fp = fopen(fastq_index_out, "w+"); 

    char *seq_id = (char *)malloc(100*sizeof(char));
    off_t entry_pos = 0;

    int id_bytes = 0;
    int entry_bytes = 0;

    //Attempt to read in first character or detect EOF
    fread(seq_id, 1, 1, in_fp); 

    while (!feof(in_fp)){

        //Read in sequence ID line
        fgets(seq_id + sizeof(char), ID_BUFFER_SIZE, in_fp); 
       
        //Get number of bytes in this line (including '\n')
        if ((id_bytes = get_id_len(seq_id, ID_BUFFER_SIZE)) == -1){
            //'\n' not found error and exit
            fprintf(stderr, "No newline found in sequence buffer\n");
            exit(1); 
        }
        
        //Get total length of entry
        entry_bytes = id_bytes + ENTRY_NO_READID_BYTES;

        //Truncate seq_id to reduce file size & later memory usage when loaded into dict
        truncate_seq_id(&seq_id, ID_BUFFER_SIZE);

        //WRITE out read id and byte offset to out_fp
        fprintf(out_fp,"%s\t%lld\n", seq_id, entry_pos);

        //Reset seq_id pointer back to start of buffer
        seq_id = seq_id - TRUNC_HEAD_SIZE;

        //in_fp currently past read id line in current entry, move in_fp to next entry
        fseek(in_fp, entry_bytes - id_bytes, SEEK_CUR);

        // Adjust entry_pos for next entry
        entry_pos += entry_bytes;

        //Try to read first character of next entry or signal EOF for feof
        //Without this fseek clears EOF and feof() will not end loop
        fread(seq_id, 1, 1, in_fp);
   }

    fclose(in_fp);
    fclose(out_fp);
}

