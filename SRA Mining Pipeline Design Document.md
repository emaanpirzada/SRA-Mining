# Integrating Metadata Filtering with the ARA Pipeline
Zoe Berge, Peyton Fay, Emaan Pirzada

Last Updated: March 16, 2026
## Overview: 
The Sequence Read Archive (SRA) is a public repository consisting of high throughput data for many samples and their sequences. It consists of different types of data including Illumina, Oxford Nanopore, PacBio, and more. They all originate from different types of metagenomic, environmental, and clinical studies allowing a broad range of information to be examined. This data can be stored in Amazon Web Services (AWS) and Google Cloud Platform (GCP) in both compressed or original formats alongside their metadata describing the sample origins and other important details. The metadata, however, is written by the researchers and can be incomplete, inconsistent, or confusing. This complex web of data and information is difficult to navigate and often dense to parse through. Although there are tool options for searching for what you need, the process is complicated and requires a lot of heavy lifting.

The ARA pipeline allows for an automated way to download, clean, and assign taxonomy to desired sequences. It allows both full and partial (screen-mode) record analysis, offering users control over data retrieval. It uses BLAST and BOWTIE2 as choices for screening the records. Trimmomatic and FastQC are used to filter low quality sequences and remove adaptors, while redundant reads are clustered using the Fastx toolkit. Additionally, it utilizes NCBI Entrez programming utilities to provide access to the sample-level metadata along with the location of the raw data stored in the cloud in case any downloading issues arise in the pipeline. Finally, it assigns taxonomic profiling using KRAKEN2.

We will develop a Python script to retrieve and parse through the latest SRA metadata file by connecting to the NCBI SRA FTP to isolate records originating from specific sample sources. The output will be a text file with one SRA accession per line. We will download, understand, and edit an already created ARA pipeline. The filtered records will then be processed through the ARA pipeline to screen for a specific query sequence of interest, enabling a targeted and efficient meta-analysis. The ARA pipeline was written in Pearl so we will instead be using Biopython and pandas for parsing through the CSV/XML metadata generated for easier function in our script.

## Context: 
The biological problem is that there is a massive amount of data in the NCBI Sequence Read Archive (SRA) makes it very challenging to conduct sequence-based searches in an efficient way, which forces researchers to rely on sometimes incomplete or inconsistent text-based metadata. This project will provide an automated, and scalable pipeline that can rapidly screen and sample SRA records to dive into specific biological content or specific genes across large datasets without the long wait time and computational costs that are present in today’s methods. 

## Goals: 
+ Develop a Python pipeline that allows researchers to search the SRA database by sample source (tissue type, environment, organism, etc.) and BLAST a query sequence against matching records using one command through the ARA pipeline.
+ Automate the retrieval, parsing, and filtering of SRA metadata so users don’t need to manually browse NCBI, accession lists, or ARA separately
+ Aggregate the BLAST results into a single summary report so users can quickly identify which samples contain hits to a gene of interest
### Non-goals:
+ No specific non-goals have currently been identified.

## Proposed Solution
+ Python script input:
  - Fasta query
  - Source of interest  
+ Python script function: 
  - Connect to the NCBI SRA FTP site to download the latest metadata file
  - Parse through this file to extract the SRA Run Accessions that match the sample source of interest
  - Begin the ARA pipeline by giving it a list of filtered accessions and the query sequence
+ Python script output/ARA input:
  - A text file containing a list of SRA run accessions to be analyzed
  - A FASTA file containing the nucleotide sequences the user is searching for within the SRA records
+ ARA pipeline will be in screening mode (look at roughly 5%) to increase speed and prevent our script from downloading unnecessary data 
+ ARA output: 
  - A summary file that ranks analyzed SRA records by their overall alignment percentage in decreasing order. It includes metadata for every accession to help users identify the most relevant samples
  - A text file detailed by the mapping tools used
  - A text file providing a classification of the reads (defaulting to a viral genomic reference)

### Pipeline Steps:
1. Parse command-line arguments
2. Retrieve metadata
3. Filter metadata
4. Run ARA
5. Aggregate results

### Workflow:


## Milestones: 
