import os
import time
from Bio import Entrez

# NCBI login
Entrez.email = "zberge@luc.edu" 

def metadata_search(sample_source, fatsa_query, output_fasta="query.fasta"):
    """
    User provides:
    1. sample_source (e.g., "wastewater" or "urine")
    2. fatsa_query (path to existing file with fasta query)
    """

    # Read the existing FASTA file
    if not os.path.exists(fatsa_query):
        print(f"Error: The file '{fatsa_query}' was not found.")
        return

    print(f"Reading query sequence from {fatsa_query}...")
    with open(fatsa_query, "r") as f_in:
        query_content = f_in.read()

    # Save a copy to the local directory to ensure the ARA pipeline can find it
    with open(output_fasta, "w") as f_out:
        f_out.write(query_content)
    
    # Search NCBI SRA for the source keyword
    # We limit to 500 to keep the ARA pipeline manageable 
    print(f"Searching NCBI SRA for source: '{sample_source}'...")
    try:
        count_handle = Entrez.esearch(db="sra", term=sample_source, retmax=0)
        count_results = Entrez.read(count_handle)
        count_handle.close()
        total = int(count_results["Count"])
        print(f"Total matching records: {total}")
        if total > 500:
            print(f"Warning: {total} total records found but capped at 500. Consider a more specific search term.")
        search_handle = Entrez.esearch(db="sra", term=sample_source, retmax=500, sort="relevance")
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        id_list = search_results["IdList"]
        print(f"Saved the top {len(id_list)} matching records at NCBI, sorted by relevance.")
    except Exception as e:
        print(f"Error during NCBI Search: {e}")
        return

    if not id_list:
        print("No records found for that source")
        return

    # Convert internal IDs to SRR Run Accessions
    print("Converting IDs to SRR Run Accessions...")
    accession_file = "matching_accessions.txt"
    run_accessions = []

    # Fetch summary info for the IDs found
    try:
        summary_handle = Entrez.esummary(db="sra", id=",".join(id_list))
        summaries = Entrez.read(summary_handle)
        summary_handle.close()

        for entry in summaries:
            # The SRR number is found inside the 'Runs' column 
            # Example: "<Run acc="SRR12345" ... />"
            # Extract the accession using split
            run_info = entry['Runs']
            if 'acc="' in run_info:
                srr = run_info.split('acc="')[1].split('"')[0]
                run_accessions.append(srr)
                
    except Exception as e:
        print(f"Error retrieving accessions: {e}")
        return

    # Save the SRR list for the ARA Pipeline
    with open(accession_file, "w") as f:
        for acc in set(run_accessions):
            f.write(f"{acc}\n")
    print(f"Saved {len(run_accessions)} accessions to {accession_file}")

'''    # Start the ARA Pipeline via Snakemake
    print("Begining ARA Pipeline for BLAST analysis...")
    # Using check=True to ensure we see errors if Snakemake fails
    import subprocess
    try:
        subprocess.run([
            "snakemake", 
            "-s", "ARA_Pipeline.smk", 
            "--config", f"list={accession_file}", f"query={output_fasta}"
        ], check=True)
    except subprocess.CalledProcessError:
        print("--- ARA Pipeline encountered an error.")'''

metadata_search("gut", "/home/epirzada/SRA-Mining/query.fasta")