(Rough Draft/Outline - Updated March 23) 

🧬 SRA-ARA Pipeline (Rough Draft - Updated March 23) 

Automating the bridge between NCBI Metadata Filtering and the ARA Pipeline.

The NCBI Sequence Read Archive (SRA) is a massive repository, but its text-based metadata is often inconsistent. This Python-driven pipeline automates the link between metadata filtering and the Automated Record Analysis (ARA) pipeline.
By allowing users to filter by sample source (e.g., "retina" or "soil") and immediately BLAST a query sequence against those specific records, we provide a scalable way to conduct targeted meta-analyses without the heavy lifting of manual data retrieval.
***
🛠️ Dependencies & Software
Python Libraries

***
💽 The Bioinformatics Toolbox

NCBI Datasets & SRA Toolkit: Programmatic metadata fetching and 5% "screen-mode" downloads.

Biopython & Pandas: Automated sequence handling and XML/CSV metadata parsing.

FastQC & Trimmomatic: Automated quality evaluation and adapter trimming.

FastX Toolkit: Sequence deduplication to reduce redundancy and accelerate analysis.

BLASTn: High-sensitivity mapping against SRA records.

Kraken2: Taxonomic classification and sample contamination detection.

***
🚀 Instructions

***
📑Input 

***
📊 Output
*** 
🔌 Example
***
🙏 Acknowledgements
Thank you to Dr. Heather Wheeler, Dr. Catherine Putonti, and the COMP 383 class members for their support and the foundational tools provided for this project.
