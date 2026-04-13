(Rough Draft/Outline - Updated March 23) 

🧬 SRA-ARA Pipeline 

Automating the bridge between NCBI Metadata Filtering and the ARA Pipeline.

The biological problem is that there is a massive amount of data in the NCBI Sequence Read Archive (SRA) makes it very challenging to conduct sequence-based searches in an efficient way, which forces researchers to rely on sometimes incomplete or inconsistent text-based metadata. This project will provide an automated, and scalable pipeline that can rapidly screen and sample SRA records to dive into specific biological content or specific genes across large datasets without the long wait time and computational costs that are present in today’s methods. 

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
🚀 Usage Instructions

***
📑Input 

***
📊 Output
*** 
🔌 Example
***
🙏 Acknowledgements

Thank you to Dr. Heather Wheeler, Dr. Catherine Putonti, and the COMP 383 class members for their support and the foundational tools provided for this project.
