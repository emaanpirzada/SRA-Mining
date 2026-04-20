"""
ARA_input.py
Retrieves SRA metadata from NCBI FTP, filters by a source keyword,
and writes the accession list + query FASTA that ARA needs.
 
Usage (standalone):
    python ARA_input.py --fasta_query my_gene.fasta --source "eyeball"
 
Usage (via Snakemake):  called automatically — see Snakefile
"""
import os
import argparse
from ftplib import FTP

def download_and_filter_sra(fasta_query, source_interest, output_list="results/accessions.txt", output_fasta="results/query.fasta"):
    """
    Connects to NCBI, filters SRA accessions by source, and prepares ARA inputs.
    """  
    ######## Below prepares the FASTA for ARA ########
    ftp_connect = "ftp.ncbi.nlm.nih.gov"
    metadata_path = "sra/reports/Metadata"
    filename = "SRA_Accessions.tab"
    #filename = "SRA_Run_Members.tab" # tab-separated and contains organism/source info 

    # Below checks if the full metadata file is downloaded 
    # IN FUTURE: and if it is up to date 
    if os.path.exists(filename):
        print(f"Local copy of '{filename}' is already downloaded.")
    else:
        ftp = FTP(ftp_connect)
        ftp.login()  #login
        ftp.cwd(metadata_path)
        print(f"New version found or file missing. Downloading {filename}...")
        #if the file doesn't exist locally
        with open(filename, "wb") as local_file: #creates a file on the local directory that deals with the binary data
            #ftp.retrbinary is used to help with the massive files by retrieving the data in binary format (zip)   
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        print("Download complete.")
        ftp.quit() #close session


    ###### Below begins to parse through the metadata

    # Save the querey
    os.makedirs(os.path.dirname(output_fasta) or ".", exist_ok=True)
    with open(fasta_query, "r") as f_in_fasta, open(output_fasta, "w") as f_out_fasta:
        f_out_fasta.write(f_in_fasta.read())


    # Parse the downloaded zip file 
    hit_count = 0
    os.makedirs(os.path.dirname(output_list) or ".", exist_ok=True)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f_in, \
         open(output_list, 'w') as f_out:
        #SRA files usually use UTF-8, specifying that tells python how to translate the binary 
        #errors='ignore' tells python to ignore weird characters that could make the code crash
        # Opens two files, first one reads metadata file and the second writes a new file  
        for line in f_in: #parses data line by line
            if source_interest.lower() in line.lower():
                columns = line.split('\t')
                # The first column is the Run Accession
                f_out.write(f"{columns[0]}\n") # Immedietly write the matching assecions txt file
                hit_count += 1

    print(f"{hit_count} accession(s) matched → {output_list}")    
    return output_list, output_fasta

##### Command-line interface ##################
def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter SRA metadata and prepare ARA inputs."
    )
    parser.add_argument(
        "--fasta_query",
        required=True,
        help="Path to query FASTA file (or raw FASTA string).",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source keyword to filter SRA records (e.g. 'eyeball', 'soil').",
    )
    parser.add_argument(
        "--output_list",
        default="results/accessions.txt",
        help="Output path for filtered accession list (default: results/accessions.txt).",
    )
    parser.add_argument(
        "--output_fasta",
        default="results/query.fasta",
        help="Output path for query FASTA copy (default: results/query.fasta).",
    )
    return parser.parse_args()
 
if __name__ == "__main__":
    args = parse_args()
    download_and_filter_sra(
        fasta_query     = args.fasta_query,
        source_interest = args.source,
        output_list     = args.output_list,
        output_fasta    = args.output_fasta,
    )