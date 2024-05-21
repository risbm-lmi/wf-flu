The script `filtered_consensus.py` serves as the foundation for one of the processes in the current workflow. This script is associated with the `process filterConsensus`, the description of which can be found in `main.nf`. 

This script generates an additional consensus sequence file, distinct from the `draft_consensus.fasta`. The output file `filtered_cons.fasta` does not contain sequences of segments whose representation in the sample data is below a threshold value set by the user via the `-t ` parameter. The `-t` parameter is required when executing the script outside the pipeline. When executed as part of nextflow command, just inside it as one of the pipeline processes (with default value 10), but you would like change  defaulte value, then please use `--tresh_lvl` parameter inside nextflow command. 

`nextflow run ./risbm-wf-flu --out_dir out_res --sample_sheet ./sample_sheets.csv --tresh_lvl 150 --disable_ping True --basecaller_cfg dna_r9.4.1_e8.1_hac_prom --fastq ./input_data -profile standard`

The `filtered_consensus.py` script can be executed outside the pipeline according to the instructions below:

usage: filtered_consensus.py [-h] -d depth.txt -c draft_consensus.fasta -t TRESHOLD [-o OUTPUT_DIR]

the following arguments are required: -d/--depth {path to file}, -c/--consensus {path to file}, -t/--treshold {integer}

If the parameter [-o OUTPUT_DIR] is not specified, the output file will be saved in the current working directory.
