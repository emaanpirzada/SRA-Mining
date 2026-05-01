# =============================================================================
# Snakemake Workflow: SRA Mining Pipeline
# Usage:
#   snakemake --cores <N> --config fasta_query=<path/to/query.fasta> source="<keyword>"
#
# Example:
#   snakemake --cores 4 --config fasta_query=my_gene.fasta source="eye"
# =============================================================================

import os
import sys

# ── Config ────────────────────────────────────────────────────────────────────
FASTA_QUERY = config.get("fasta_query", None)
SOURCE      = config.get("source",      None)

# Validate required inputs up front so errors are clear
if not FASTA_QUERY or not SOURCE:
    sys.exit(
        "\n[ERROR] Both 'fasta_query' and 'source' must be provided via --config.\n"
        "  Example: snakemake --cores 4 "
        "--config fasta_query=my_gene.fasta source=\"eyeball\"\n"
    )

if not os.path.exists(FASTA_QUERY):
    sys.exit(f"\n[ERROR] Query FASTA file not found: {FASTA_QUERY}\n")

# ── Output paths ──────────────────────────────────────────────────────────────
ACCESSIONS  = "results/accessions.txt"         # filtered SRA accession list
QUERY_COPY  = "results/query.fasta"            # copy of query fasta used by ARA
ARA_DONE    = "results/ara/ara_complete.done"  # sentinel: ARA finished
ARA_SUMMARY = "results/summary/summary.txt"    # final human-readable summary

# =============================================================================
# Rule: all — top-level target
# =============================================================================
rule all:
    input:
        ARA_SUMMARY

# =============================================================================
# Rule: prepare_inputs
#   Calls ARA_input.py to:
#     1. Download / reuse SRA_Accessions.tab from NCBI FTP
#     2. Filter rows matching SOURCE keyword
#     3. Write accessions.txt and query.fasta into results/
# =============================================================================
rule prepare_inputs:
    output:
        accessions = ACCESSIONS,
        query      = QUERY_COPY
    params:
        fasta_query = FASTA_QUERY,
        source      = SOURCE,
        retmax      = config.get("retmax", 500)
    log:
        "logs/prepare_inputs.log"
    shell:
        """
        mkdir -p results logs
        python ARA_input.py \
            --fasta_query  {params.fasta_query} \
            --source       "{params.source}" \
            --output_list  {output.accessions} \
            --output_fasta {output.query} \
            --retmax       {params.retmax} \
            > {log} 2>&1
        """

# =============================================================================
# Rule: check_accessions
#   Validates that the filtered accession list is non-empty before continuing.
#   Failing here gives an error instead of a crash.
# =============================================================================
rule check_accessions:
    input:
        ACCESSIONS
    output:
        temp("results/accessions_validated.flag")
    run:
        with open(input[0]) as fh:
            lines = [l.strip() for l in fh if l.strip()]
        if not lines:
            sys.exit(
                f"\n[ERROR] No SRA accessions matched source keyword: '{SOURCE}'.\n"
                "  Try a broader keyword or check SRA_Accessions.tab manually.\n"
            )
        print(f"[OK] {len(lines)} accession(s) matched '{SOURCE}'.")
        with open(output[0], "w") as flag:
            flag.write(str(len(lines)))

# =============================================================================
# Rule: run_ara
#   Passes the accession list and query FASTA to the ARA pipeline.
# =============================================================================
rule run_ara:
    input:
        accessions = ACCESSIONS,
        query      = QUERY_COPY,
        validated  = "results/accessions_validated.flag"
    output:
        done = ARA_DONE
    params:
        ara_outdir = "results/ara",
        ara_dir    = config.get("ara_dir", "ARA"),
        threads    = config.get("threads", 4)
    log:
        "logs/ara.log"
    shell:
        """
        mkdir -p {params.ara_outdir}

        perl {params.ara_dir}/ara.pl \
            --input     {input.accessions} \
            --sequences {input.query} \
            --output    {params.ara_outdir} \
            --mode      screen \
            --threads   {params.threads} \
            > {log} 2>&1

        touch {output.done}
        """

# =============================================================================
# Rule: summarize
#   Collects ARA result files and writes a tidy summary report.
# =============================================================================
rule summarize:
    input:
        done       = ARA_DONE,
        accessions = ACCESSIONS,
        query      = QUERY_COPY
    output:
        ARA_SUMMARY
    params:
        ara_outdir = "results/ara",
        ara_dir    = config.get("ara_dir", "ARA"),
        source     = SOURCE
    run:
        import glob
        from datetime import datetime

        with open(input.accessions) as fh:
            accession_list = [l.strip() for l in fh if l.strip()]

        # Collect any TSV/CSV hit files ARA produced
        hit_files = (
            glob.glob(os.path.join(params.ara_outdir, "**", "*.txt"), recursive=True) +
            glob.glob(os.path.join(params.ara_outdir, "**", "*.tsv"), recursive=True) +
            glob.glob(os.path.join(params.ara_outdir, "**", "*.csv"), recursive=True)
        )

        total_hits = 0
        for hf in hit_files:
            with open(hf) as fh:
                total_hits += max(0, sum(1 for l in fh if l.strip()) - 1)  # subtract header

        os.makedirs("results/summary", exist_ok=True)
        with open(output[0], "w") as out:
            out.write("=" * 60 + "\n")
            out.write("  SRA Mining Pipeline — Summary Report\n")
            out.write("=" * 60 + "\n")
            out.write(f"  Run date        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"  Source keyword  : {params.source}\n")
            out.write(f"  Query FASTA     : {input.query}\n")
            out.write(f"  Accessions found: {len(accession_list)}\n")
            out.write(f"  ARA hit files   : {len(hit_files)}\n")
            out.write(f"  Total BLAST hits: {total_hits}\n")
            out.write("=" * 60 + "\n\n")
            out.write("Accessions queried:\n")
            for acc in accession_list:
                out.write(f"  {acc}\n")
            out.write("\nARA output files:\n")
            for hf in hit_files:
                out.write(f"  {hf}\n")

        print(f"\n[Done] Summary written to {output[0]}")
        print(f"       {len(accession_list)} accessions | {total_hits} BLAST hits")