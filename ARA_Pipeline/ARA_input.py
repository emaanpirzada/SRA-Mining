import os
import gzip
from ftplib import FTP

def download_and_filter_sra(fasta_query, source_interest, output_list="accessions.txt", output_fasta="query.fasta"):
    """
    Connects to NCBI, filters SRA accessions by source, and prepares ARA inputs.
    """
    ftp_connect = "ftp.ncbi.nlm.nih.gov"
    metadata_data = "sra/reports/Metadata"
    filename = "SRA_Run_Members.gz"  # Common metadata file
    
    ftp = FTP(ftp_connect)
    ftp.login()  #login
    ftp.cwd(metadata_data)

    ######## Bellow prepares the FASTA for ARA #######
    
    # Save the querey
    with open(output_fasta, "w") as f:
        f.write(fasta_query)
    
    ###### Bellow begins to parse through the metadata
    
    accessions = [] #list of sccession numbers 
    
    # This is a function to work with the metadata file part by part in order to reduce dowloading the entire file  
    def process_line(line):
        # gets every line that has the sample source in it 
        if source_interest.lower() in line.lower(): #.lower turns every character into lowercase to reduce conflict
            parts = line.split('\t') #splits data based on tab (line by line)
            # SRR is the first column in run assesions
            if parts[0].startswith(("SRR")): #check first part to ensure its the SRR in the Sequence Read Archive
                accessions.append(parts[0]) #if its a SRR number, it adds it to the growing list of acession numbers  

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

# Example usage:
# fasta_content = ">Query1\nATGC..."
# download_and_filter_sra(fasta_content, "Homo sapiens")