import os

# ──────────────────────────────────────────────
# Read config from command line
# ──────────────────────────────────────────────
QUERY       = config["query"]
SOURCE      = config["source"]
BLAST_TYPE  = config.get("blast_type", "blastn")
MODE        = config.get("mode", "screen")
THREADS     = int(config.get("threads", 4))
OUTDIR      = config.get("outdir", "results")
MAX_ACC     = config.get("max_accessions", None)

# Path to ARA (relative to Snakefile location)
ARA_DIR = os.path.join(workflow.basedir, "ARA")

# ──────────────────────────────────────────────
# Target rule
# ──────────────────────────────────────────────
rule all:
    input:
        os.path.join(OUTDIR, "pipeline_complete.flag")


# ──────────────────────────────────────────────
# Rule 1: Download SRA metadata & filter by source
# ──────────────────────────────────────────────
rule download_and_filter:
    output:
        accession_list = os.path.join(OUTDIR, "accessions.txt")
    params:
        source         = SOURCE,
        max_accessions = MAX_ACC
    log:
        os.path.join(OUTDIR, "logs", "download_filter.log")
    script:
        "ARA_input.py"


# ──────────────────────────────────────────────
# Rule 2: Run ARA (BLAST only)
# ──────────────────────────────────────────────
rule run_ara:
    input:
        accession_list = os.path.join(OUTDIR, "accessions.txt"),
        query          = QUERY
    output:
        flag = os.path.join(OUTDIR, "pipeline_complete.flag")
    params:
        ara_dir  = ARA_DIR,
        outdir   = OUTDIR,
        mode     = MODE,
        config   = os.path.join(ARA_DIR, "conf.txt")
    threads: THREADS
    log:
        os.path.join(OUTDIR, "logs", "ara.log")
    shell:
        """
        perl {params.ara_dir}/ara.pl \
            --input {input.accession_list} \
            --sequences {input.query} \
            --output {params.outdir}/ara_output \
            --mode {params.mode} \
            --config {params.config} \
            2>&1 | tee {log}

        touch {output.flag}
        """