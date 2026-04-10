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

from Bio import Entrez

def get_srr_by_source(sample_source, email, limit=10):
    Entrez.email = email

    # Search for SRA records matching the source
    search_handle = Entrez.esearch(db="sra", term=sample_source, retmax=limit)
    search_results = Entrez.read(search_handle)
    search_handle.close()

    ids = search_results.get("IdList", [])
    
    # Get the actual SRR numbers for those IDs
    fetch_handle = Entrez.efetch(db="sra", id=",".join(ids), rettype="runinfo", retmode="text")
    run_info = fetch_handle.read()
    fetch_handle.close()
    
    # Extract SRR numbers (usually the first column of the runinfo CSV)
    accessions = [line.split(',')[0] for line in run_info.split('\n') if line.startswith(('SRR', 'ERR', 'DRR'))]

    #write file with accession number for ARA
    with open("matched_accessions.txt", "w") as f:
        f.write("\n".join(accessions))
        
    return accessions
