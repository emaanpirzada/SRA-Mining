(Rough Draft - Updated March 23) 

🧬 SRA-ARA Pipeline (Rough Draft - Updated March 23) 

Automating the bridge between NCBI Metadata Filtering and the ARA Pipeline.

The NCBI Sequence Read Archive (SRA) is a massive repository, but its text-based metadata is often inconsistent. This Python-driven pipeline automates the link between metadata filtering and the Automated Record Analysis (ARA) pipeline.
By allowing users to filter by sample source (e.g., "retina" or "soil") and immediately BLAST a query sequence against those specific records, we provide a scalable way to conduct targeted meta-analyses without the heavy lifting of manual data retrieval.
***
🛠️ Dependencies & Software
Python Libraries

Library	Purposes
Pandas	Parsing and filtering the large SRA_Accessions.tab file.
Biopython	Handling FASTA query files and NCBI Entrez utilities.
Bioinformatics Tools

ARA Pipeline: The core analysis engine (Perl) for record screening.

SRA Toolkit: For downloading raw reads (prefetch and fasterq-dump).

Kraken2: For taxonomic profiling of reads.
***
🚀 Instructions

***
📊 Output

***
🙏 Acknowledgements
Thank you to Dr. Heather Wheeler, Dr. Catherine Putonti, and the COMP 383 class members for their support and the foundational tools provided for this project.
