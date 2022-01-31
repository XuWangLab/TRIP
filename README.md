# TRIP
***TRIP*** is **a pipeline for identifying the TRM (telomeric repeat motif) using short-read genome sequencing data**. 

***TRIP*** is designed to take advantage of short-read data that are publicly available or generated by the users (local data). 

For public data, a table of accession numbers needs to be provided, with specified number of processes ***LARGE*** `--process_num`.

For interupted runs, set `--continue True` to resume the pipeline. If the computation time is too long, you can use `--downsample` to limit download size and save time.

# Installation
0. **Prerequisite** 
- Linux system (not supporting Windows.)
- **weget, python3, bash, tail, cat, rm** commands should be able to be called.
- **matplotlib
    multiprocessing
    os
    sys
    pandas
    inspect
    numpy
    requests
    random
    bs4
    time
    traceback
    multiprocessing
    hashlib** package should be installed in python3.

1. Download the code. ***Do not change the content in the folder***.

2. `chmod -R 777 /path/to/TRIP` Try to run `RepeatDetector_v2` in ***TRIP***, if you see 
```
***********************************
* RepeatDetector                  *
* author: Yi Wang                 *
* email:  godspeed_china@yeah.net *
* date:   29/May/2018             *
***********************************
``` 
rather than `pemission denied`, then you should be cool.

# Basic usage (pipeline of auto: web-crawl > download reads > analyze > filter results > output plots and tables)
## command line
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

## input file
***TRIP*** will parse the input file (make sure your input file is the same format as example_input.tsv). Each row in input file is a sample. 

The **NAME** column should be unique.

The **BIOPROJECT** column should be correct， otherwise ***TRIP*** cannot process the corresponding sample. The definition of **BIOPROJECT** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/bioproject/). ***TRIP*** needs this to download reads.

The **ASSEMBLY** column should be correct, otherwise ***TRIP*** cannot process corresponding sample. The definition of **ASSEMBLY** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/assembly). ***TRIP*** needs this to get genome size for further computation.

In **example_input.tsv**, we have 2 samples to check. One is CARCR (Cariama cristata), another is HARAX (Harmonia axyridis). For CARCR, the BIOPROJECT  is [PRJNA212889](https://www.ebi.ac.uk/ena/browser/view/PRJNA212889?show=reads), the ASSEMBLY is [GCA_000690535.1](https://www.ncbi.nlm.nih.gov/assembly/GCA_000690535.1) (GCF_000690535.1 also works). 

## output files
```
test
└── [4.0K Jan 23  0:14]  TRIP_results
    ├── [4.0K Jan 23  0:14]  barplots
    │?? ├── [376K Jan 23  0:14]  CARCR_percent_repeats_len_per_read.pdf
    │?? ├── [377K Jan 23  0:14]  CARCR_percent_repeat_unit_in_sequences.pdf
    │?? ├── [377K Jan 23  0:14]  CARCR_repeats_len_per_genome.pdf
    │?? ├── [377K Jan 23  0:14]  CARCR_repeats_len_per_million_reads.pdf
    │?? ├── [376K Jan 22 23:23]  HARAX_percent_repeats_len_per_read.pdf
    │?? ├── [377K Jan 22 23:23]  HARAX_percent_repeat_unit_in_sequences.pdf
    │?? ├── [377K Jan 22 23:23]  HARAX_repeats_len_per_genome.pdf
    │?? └── [377K Jan 22 23:23]  HARAX_repeats_len_per_million_reads.pdf
    ├── [4.0K Jan 23  0:12]  CARCR
    │?? ├── [ 617 Jan 22 19:17]  CARCR_PRJNA212889_tsv.txt
    │?? ├── [6.7M Jan 23  0:12]  CARCR.repeat
    │?? ├── [651K Jan 23  0:12]  CARCR_repeatsummary.tsv
    │?? ├── [  32 Jan 23  0:12]  CARCR.stat
    │?? ├── [  90 Jan 23  0:12]  CRPG_input.tsv
    │?? ├── [ 410 Jan 22 19:17]  ENA2URL.sh
    │?? ├── [  10 Jan 23  0:03]  genome_size
    │?? ├── [  32 Jan 23  0:02]  md5_log
    │?? ├── [261M Jan 22 20:04]  SRR953484_1.fastq.gz
    │?? ├── [1.0G Jan 22 22:34]  SRR953484_2.fastq.gz
    │?? ├── [816M Jan 22 21:04]  SRR953485_1.fastq.gz
    │?? ├── [1.5G Jan 22 23:42]  SRR953485_2.fastq.gz
    │?? ├── [ 268 Jan 22 19:17]  url
    │?? ├── [ 268 Jan 22 19:17]  url_filtered
    │?? └── [ 209 Jan 22 19:17]  wget.sh
    ├── [4.0K Jan 23  0:14]  filtered_tables
    │?? ├── [ 73K Jan 23  0:14]  CARCR_output.csv
    │?? └── [ 42K Jan 22 23:23]  HARAX_output.csv
    ├── [4.0K Jan 22 23:22]  HARAX
    │?? ├── [  90 Jan 22 23:22]  CRPG_input.tsv
    │?? ├── [2.0G Jun  8  2020]  DRR100149_1.fastq.gz
    │?? ├── [2.0G Jun  6  2020]  DRR100150_1.fastq.gz
    │?? ├── [2.2G Jun  6  2020]  DRR100150_2.fastq.gz
    │?? ├── [201M Jan 22 21:11]  DRR100152_2.fastq.gz
    │?? ├── [ 410 Jan 22 19:17]  ENA2URL.sh
    │?? ├── [   9 Jan 22 23:00]  genome_size
    │?? ├── [1.1K Jan 22 19:17]  HARAX_PRJDB6162_tsv.txt
    │?? ├── [ 16M Jan 22 23:22]  HARAX.repeat
    │?? ├── [405K Jan 22 23:22]  HARAX_repeatsummary.tsv
    │?? ├── [  32 Jan 22 23:22]  HARAX.stat
    │?? ├── [  32 Jan 22 23:00]  md5_log
    │?? ├── [ 536 Jan 22 19:17]  url
    │?? ├── [ 268 Jan 22 19:17]  url_filtered
    │?? └── [ 209 Jan 22 19:17]  wget.sh
    ├── [4.0K Jan 23  0:14]  TR_candidates
    │?? ├── [ 65K Jan 23  0:14]  CARCR_output.csv.0.filtered.xlsx
    │?? ├── [ 43K Jan 23  0:14]  HARAX_output.csv.1.filtered.xlsx
    │?? ├── [6.0K Jan 23  0:14]  TR_candidates.qualified.dominant.xlsx
    │?? └── [5.9K Jan 23  0:14]  TR_candidates.qualified.xlsx
    └── [ 932 Jan 23  0:14]  TRIP.log.csv
```
The output files can be downloaded in [BOX](https://auburn.box.com/s/kuy0i0j9x0hr26uz730035xwexwb1s74)
### `TRIP_results/each_sample` : 
- each sample has one independent folder.
- `CARCR_PRJNA212889_tsv.txt` is the downloaded reads records file
- `CARCR.repeat CARCR.repeatsummary.tsv and CARCR.stat` are the ***RepeatMaster*** processed results 
- `ENA2URL.sh  genome_size  md5_log  url  url_filtered  wget.sh` are intermediate files. `url` records all the reads urls of corresponding sample. `url_filtered` records the reads that will be downloaded and processed by ***TRIP*** (downsampled to save time), you can manually modify `url_filtered` if needed.
- `SRR9946514_2.fastq.gz SRR9946514_1.fastq.gz` are downloaded reads
- CRPG_input.tsv is file that will pass to `cal_repeats_per_genome_and_percent_of_len_linux.py` in ***TRIP***
### `TRIP_results/filtered_tables`:
- `*_output.csv` include all the parameters ***TRIP*** calculated for each sample. The column names are easy to understand. You can also refer to our article for more details.
### `TRIP_results/TR_candidates` :
- `TR_candidates.qualified.xlsx` includes TRM candidates that passed the 5 hard-cut-off
- `TR_candidates.qualified.dominant.xlsx` includes TRM candidates that passed the 5 hard-cut-off and **dominant** criteria. 
- ***NOTICE***, ***TRIP*** also recommend **support** criteria, which means, the TRM candidate in `TR_candidates.qualified.dominant.xlsx`, should have same candidate from same family species, or other experiment, or genome assembly, as the support. For example, you found a novel TRM in species1, and no one reported it before. You should use ***TRIP*** to identify the same TRM in another same-family-species2, to support each other. This is important to exclude false positive cases.
### `TRIP_results/barplots`: 
- barplots of 4 parameters which can be used for publication. 
- ***NOTICE***, **AACCT** is equivalent to **TTAGG**, because DNA is reverse complementary pairing.
- In example, ***TRIP*** didn't identify the TRM of CARCR, but from the barplots, we can see **AACCCT** is outstanding. Therefore, a great probability of **TTAGGG** as TRM. In such condition, users should finish downloading the reads files of CARCR and re-run ***TRIP***.

# Usage on local data
## command line
Users need to understand the structure of ***TRIP***. Read **TRIP structure**.

Firstly, run `module4.py`
> `python3 path/to/TRIP/module_4.py path/to/TRIP/RepeatDetector_v2 path/to/TRIP/RepeatSummary_v2 path/to/TRIP_results/CARCR/CARCR 1 25 16 path/to/TRIP_results/CARCR/SRR953484_2.fastq.gz path/to/TRIP_results/CARCR/SRR953485_2.fastq.gz path/to/TRIP_results/CARCR/SRR953484_1.fastq.gz path/to/TRIP_results/CARCR/SRR953485_1.fastq.gz path/to/TRIP_results/CARCR/CARCR_repeatsummary.tsv path/to/TRIP_results/CARCR/CARCR.repeat`

> `1,25,16` are the -r,-R,-n parameters of RepeatDetector_v2
> ***TRIP*** take all reads as single end reads.

Then, run `module5.py`
> `python3 path/to/TRIP/module_5.py path/to/TRIP/cal_repeats_per_genome_and_percent_of_len_linux.py HARAX path/to/TRIP_results/CARCR parent_dir_of_TRIP_results/(which is test/ in this case)`

> `cal_repeats_per_genome_and_percent_of_len_linux.py` for caculations and plots.

Finally, run `module6.py`
> `python3 path/to/TRIP/module_6.py path/to/TRIP_results/filtered_tables 12000 0 0 4 0 0 10 0 0 0 0 0 0 4 0.5 0 0 3 999 path/to/TRIP_results/TR_candidates path/to/TRIP/filter_output_tables_to_xlsx.py`

> `12000 0 0 4 0 0 10 0 0 0 0 0 0 4 0.5 0 0 3 999` are the parameters/threshould. Check module_6.py source code, or see ***TRIP*** help manual.
> `filter_output_tables_to_xlsx.py` to filter the results using 5-hard-cut-off and criteria 1.

# TRIP structure
```
## module 1
Given the NAME column and output_dir, check whether name-folder exists (delete if exists),
otherwise, create it. Create processed_tables folder in the working dir to store tables processed from
repeatmaster output. Create barplots folder to store 4 types of barplots generated
from proccessed tables. Create filtered_tables to store filtered tables from
processed tables. Create manual.txt to record failed NAMEs for further manual
processing.

for each thread:
    ## module 2
    Given the BIOPROJECT, download the record file from ENA database to the
    name-folder. Then use parsing script to extract FASTQ file FTP locations.
    Download the FASTQ files to the name-folder.
    ## module 3
    Given the ASSEMBLY, web-scrap the "Total ungapped length" from NCBI website.
    Write the genome_size to genome_size file in name-folder.
    ## module 4
    Given the dir to repeatmaster (come with TRIP), process the FASTQ files in name-folder
    and generate intermediates into name-folder.
    ## module 5
    Process the repeatmaster output tables and store filtered tables into filtered_tables.
    Store barplots into barplots folder.

## module 6
Given the filtration parameters to filter the processed tables in processed_tables
and generate the TRM candidates folder to store TRM candidates.

```
We suggest users to read original code when needed.

# Q&A
***Why my TRIP seems not to be running?***

At beginning, you may observe no running via `htop` or other background-check command, which is because TRIP is downloading files. You can use `tree path/to/TRIP_results` to check files current status simutaneously, the `wget` method built-in TRIP consumes neglectable computing resources.

***Can TRIP handle long sequencing reads?***

We haven't tested it. But we offer `--skip_subreads`, which will let ***TRIP*** skip reads names containing "subreads". Usually, file names containing "subreads" means long sequencing reads.

***TRIP didn't finish downloading the reads?***

This may happen because of local connection internet limitations and you may need to re-try downloading (just re-run the ***TRIP***). However, even with truncated reads file, ***TRIP*** ususally can still identify the correct TRM. For example, in the ***output file*** section above, our downloads also truncated, but ***TRIP*** still identified the **AACCT** in HARAX. On the other hand, you can still re-run the ***TRIP*** with `--continue True`, ***TRIP*** will continue from the truncated downloads.
