import os
import gzip
from ftplib import FTP

def download_and_filter_sra(fasta_query, source_interest, output_list="accessions.txt", output_fasta="query.fasta"):
    """
    Connects to NCBI, filters SRA accessions by source, and prepares ARA inputs.
    """  
    ######## Bellow prepares the FASTA for ARA #######

    filename = ''
    
    ### add a check to see if the metadata is already download and if the version is up to date #### 
    ### add a filter that only grabs high quality reads 

    ftp_connect = "ftp.ncbi.nlm.nih.gov"
    metadata_path = "sra/reports/Metadata"

    ftp = FTP(ftp_connect)
    ftp.login()  #login
    ftp.cwd(metadata_path)
    ftp_dir = ftp.nlst()

    full_files = []
    start_chars = 'Full_'
    end_chars = '.tar.gz'
    most_recent = 0

    for i in ftp_dir: 
        if 'NCBI_SRA_Metadata_Full_' in i:
            date = int(i.split(start_chars)[1].split(end_chars)[0])
            if date > most_recent:
                most_recent = date
            full_files.append(i)

    for i in full_files:
        if str(most_recent) in i:
            filename = i 
    
    # Save the querey
    with open(output_fasta, "w") as f:
        f.write(fasta_query)
    
    ###### Bellow begins to parse through the metadata
                
    with open(filename, "wb") as local_file: #creates a file on the local directory that deals with the binary data
        #ftp.retrbinary is used to help with the massive files by retrieving the data in binary format (zip)   
        ftp.retrbinary(f"RETR {filename}", local_file.write) 
    ftp.quit() #close session

    # Parse the downloaded zip file 
    filtered_runs = [] #list of filtered and downloaded runs 
    with gzip.open(filename, 'rt') as f: #rt lets python decompress the binary data into readable text strings as it reads
        for line in f: #parses data line by line 
            if source_interest.lower() in line.lower():
                column = line.split('\t')
                filtered_runs.append(column[0]) 

    # Save Output
    with open(output_list, "w") as f:
        for run in filtered_runs:
            f.write(f"{run}\n")

    return output_list, output_fasta

download_and_filter_sra ("/home/zberge/ARA_Pipeline/example.fasta", "Homo sapiens")


