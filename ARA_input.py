import tarfile
import os
import io
import gzip
from ftplib import FTP

def download_and_filter_sra(fasta_query, source_interest, output_list="accessions.txt", output_fasta="query.fasta"):
    """
    Connects to NCBI, filters SRA accessions by source, and prepares ARA inputs.
    """  
    ######## Bellow prepares the FASTA for ARA #######

    filename = ''

    ftp_connect = "ftp.ncbi.nlm.nih.gov"
    metadata_path = "sra/reports/Metadata"
    metadata_path = "sra/reports/Metadata"
    filename = "SRA_Run_Members.gz" # Or SRA_Full_Report.gz

    ftp = FTP(ftp_connect)
    ftp.login()  #login
    ftp.cwd(metadata_path)
    ftp_dir = ftp.nlst()

    start_chars = 'Full_'
    end_chars = '.tar.gz'
    most_recent = 0

    for i in ftp_dir: 
        if 'NCBI_SRA_Metadata_Full_' in i:
            date = int(i.split(start_chars)[1].split(end_chars)[0])
            if date > most_recent:
                most_recent = date

    filename = f"NCBI_SRA_Metadata_Full_{most_recent}.tar.gz"
    
    # Save the querey
    with open(output_fasta, "w") as f:
        f.write(fasta_query)

    # Bellow checks if the full file is downloaded and if it is up to date 
    if os.path.exists(filename):
        print(f"Local copy '{filename}' is already up to date. Skipping download.")
    else:
        print(f"New version found or file missing. Downloading {filename}...")
        #if the file doesn't exist locally
        with open(filename, "wb") as local_file: #creates a file on the local directory that deals with the binary data
            #ftp.retrbinary is used to help with the massive files by retrieving the data in binary format (zip)   
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        print("Download complete.")

    ftp.quit() #close session
    
    ###### Bellow begins to parse through the metadata
 
    '''# Parse the downloaded zip file 
    filtered_runs = [] #list of filtered and downloaded runs 
    with gzip.open(filename, 'rt') as f: #rt lets python decompress the binary data into readable text strings as it reads
        for line in f: #parses data line by line 
            if source_interest.lower() in line.lower():
                column = line.split('\t')
                filtered_runs.append(column[0]) '''

    # Parse the downloaded file
    filtered_runs = []
    
    print(f"Opening Tarball: {filename}")
    with tarfile.open(filename, "r:gz") as tar:
        # Loop through every file inside the tarball to look for target source 
        for member in tar:
            # skip directories
            if member.isfile():
                f = tar.extractfile(member)
                if f:
                    # We decode each small file and check for your interest
                    content = f.read().decode('utf-8', errors='ignore')
                    if source_interest.lower() in content.lower():
                        # Using the filename as the accession if it's the run ID
                        filtered_runs.append(member.name)
        
    print(f"Found {len(filtered_runs)} matches.")
    
    # Save Output
    print("Wrighting out the filtered runs")
    with open(output_list, "w") as f:
        for run in filtered_runs:
            f.write(f"{run}\n")

    return output_list, output_fasta

download_and_filter_sra ("/home/zberge/ARA_Pipeline/example.fasta", "Homo sapiens")
