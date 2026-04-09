import os
from ftplib import FTP

def download_and_filter_sra(fasta_query, source_interest, output_list="accessions.txt", output_fasta="query.fasta"):
    """
    Connects to NCBI, filters SRA accessions by source, and prepares ARA inputs.
    """  
    ######## Bellow prepares the FASTA for ARA #######

    ftp_connect = "ftp.ncbi.nlm.nih.gov"
    metadata_path = "sra/reports/Metadata"

    ftp = FTP(ftp_connect)
    ftp.login()  #login
    ftp.cwd(metadata_path)

    #filename = "SRA_Run_Members.tab" # tab-separated and contains organism/source info 
    filename = "SRA_Accessions.tab"

    # Save the querey
    with open(output_fasta, "w") as f:
        f.write(fasta_query)

    # Bellow checks if the full file is downloaded and if it is up to date 
    if os.path.exists(filename):
        print(f"Local copy of '{filename}' is already downloaded.")
    else:
        print(f"New version found or file missing. Downloading {filename}...")
        #if the file doesn't exist locally
        with open(filename, "wb") as local_file: #creates a file on the local directory that deals with the binary data
            #ftp.retrbinary is used to help with the massive files by retrieving the data in binary format (zip)   
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        print("Download complete.")

    ftp.quit() #close session
    
    ###### Bellow begins to parse through the metadata
 
    # Parse the downloaded zip file 

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
        
    return output_list, output_fasta

download_and_filter_sra ("/home/zberge/ARA_Pipeline/example.fasta", "Homo Sapien")
