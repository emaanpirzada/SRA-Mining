import subprocess
import sys
import os

def ara_pipeline_input(query_fasta, sample_source, limit=5):
    
    #use esearch to find the samples and efetch to get the 'runinfo' csv
    #filter for the first column(Run ID) and only keep rows starting with 'SRR'
    search_cmd = (
        f'esearch -db sra -query "{sample_source}" | '
        f'efetch -format runinfo | cut -d "," -f 1 | grep "SRR" | head -n {limit}'
    )
    
    #search and capture output
    result = subprocess.check_output(search_cmd, shell=True).decode('utf-8')
    #utf-8 is binary version of the data 
    accessions = result.strip().split('\n')
    
    #write file with accession number for ARA
    with open("matched_accessions.txt", "w") as f:
        f.write("\n".join(accessions))

