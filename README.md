🧬 SRA-ARA Pipeline 

Automating the bridge between NCBI Metadata Filtering and the ARA Pipeline.

The biological problem is that there is a massive amount of data in the NCBI Sequence Read Archive (SRA) makes it very challenging to conduct sequence-based searches in an efficient way, which forces researchers to rely on sometimes incomplete or inconsistent text-based metadata. This project will provide an automated, and scalable pipeline that can rapidly screen and sample SRA records to dive into specific biological content or specific genes across large datasets without the long wait time and computational costs that are present in today’s methods. 
***
Cloning the environment

Method 1: Using the Command Palette (Fastest)

Open VS Code.

Press Ctrl + Shift + P (Windows/Linux) or Cmd + Shift + P (macOS) to open the Command Palette.

Type "Git: Clone" and select it.

Paste the repository URL you copied from GitHub into the text box that appears at the top.

Press Enter.

VS Code will prompt you to select a local folder on your computer where you want the project to be saved.

Once the download finishes, VS Code will ask if you want to "Open" the newly cloned folder. Click Open.

Method 2: Using the Source Control Tab

On the left-hand sidebar of VS Code, click the Source Control icon (it looks like a branch node).

Click the "Clone Repository" button that appears.

Choose "Clone from GitHub".

Note: If this is your first time, VS Code may ask you to sign in to your GitHub account to authorize the connection.

A dropdown list of your repositories (or those you have access to) will appear at the top. Select the one you want.

Select the destination folder on your machine, and the project will clone automatically.
***
🛠️ Dependencies & Software
Python Libraries

1. Python Libraries (Data Retrieval)

The metadata retrieval script (ARA_input.py) requires the following:

**Biopython**: Used for interacting with the NCBI Entrez API to search SRA and retrieve metadata.

Install: pip install biopython

**NumPy**: Handles numerical operations required during data processing.

Install: pip install numpy

2. Bioinformatics Workflow Tools (Execution)

The analysis workflow (Snakefile) relies on the following tools:

**Snakemake**: The primary workflow management system that orchestrates data processing.

Install: conda install -c bioconda snakemake

**NCBI SRA Toolkit**: Used for downloading and converting the raw sequencing data.

Install: conda install -c bioconda sra-tools

***
💽 The Bioinformatics Toolbox

NCBI Datasets & SRA Toolkit: Programmatic metadata fetching and 5% "screen-mode" downloads.

Biopython & Pandas: Automated sequence handling and XML/CSV metadata parsing.

FastQC & Trimmomatic: Automated quality evaluation and adapter trimming.

FastX Toolkit: Sequence deduplication to reduce redundancy and accelerate analysis.

BLASTn: High-sensitivity mapping against SRA records.

Kraken2: Taxonomic classification and sample contamination detection.

***
📑Input 

To initiate the analysis, the following inputs are required:

Source Keyword **(--source)**: A string representing the environment, organism, or sample type you wish to mine from the NCBI Sequence Read Archive (e.g., "Enterococcus", "wastewater", "human gut").

Query Sequence **(--fasta_query)**: A file in FASTA format containing the specific gene or sequence fragment you are searching for across the retrieved datasets.

***
📊 Output

query.fasta	--> A local copy of your input sequence -->	Used as the reference for downstream BLAST or alignment analysis.

matching_accessions.txt -->	A plain-text file containing a list of SRA Run (SRR) accessions -->	The "to-do list" used by Snakemake to process the data

ARA/ -->	A directory containing the results of the Snakemake execution -->	Stores the final bioinformatics outputs (e.g., alignments, count matrices, or filtered sequences).
*** 
🔌 Example

1. The Input Query (**example.fasta**):
Use this FASTA-formatted file as your search target:

Code snippet
>vanA_marker_fragment
ATGAATAGAATAAAAGTTGCAATAGAAGTTTATAGCACAACCGTTACTTCTGATGAATTG
GAAAAAATACAAGGATATCATCAATTTATTCGTCCTGAATGGATAGTTTATCAAGGTGCA
ACTTTGATTAATCAAGTTATTCAATATATAGTAGGAAGAGTTGCTGAAAAA

2. Step 1: Metadata Retrieval
Execute this command to search NCBI and generate your target list:

Bash
**python ARA_input.py --source "Enterococcus" --fasta_query "example.fasta"**

Result: Generates matching_accessions.txt (a list of 10 SRR accessions) and query.fasta.

***
🙏 Acknowledgements

Thank you to Dr. Heather Wheeler, Dr. Catherine Putonti, and the COMP 383 class members for their support and the foundational tools provided for this project.
