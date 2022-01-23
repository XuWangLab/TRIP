# TRIP
***TRIP*** is **a pipeline for identifying the TRM (telomeric repeat motif. e.g, (TTAGG)n in most insects and (TTAGGG)n in verterbrates) using NGS short reads (DNA)**. 

TRIP is ultra-fast, easy-to-use, and accurate. During our test in more than 100 species, ***TRIP*** successfully identified several unexpected novel TRM, all known TRM, with no false-positive case. For species which has no TRM (Dipteran, etc), ***TRIP*** smartly will identify 0 TRM candidates.

***TRIP*** is designed to be able to take advantage of all public data. Therefore, the basic usage of ***TRIP*** is just to provide a table, using default parameters, set a ***LARGE*** `--process_num` (the calculation of ***TRIP*** is very small, the bottleneck is actually the downloading speed from NCBI/ENA database), run it in background, and enjoy the rest of your life. To make life easier, ***TRIP*** also set `--continue True` as default, so you don't have to worry about any failure, just re-run it if needed. Since most public data is huge, you can use `--downsample` to limit download size and save time (usually, 4 good NGS reads in good quality is deep enough to identify the TRM).

# Installation
0. **Pre-needed** 
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

1. Download the code and store the code folder in someplace. ***Do not change the content in the folder***.

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

The **BIOPROJECT** column should be correct， otherwise ***TRIP*** cannot process corresponding sample. The definition of **BIOPROJECT** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/bioproject/). ***TRIP*** need this to download reads.

The **ASSEMBLY** column should be correct, otherwise ***TRIP*** cannot process corresponding sample. The definition of **ASSEMBLY** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/assembly). ***TRIP*** need this to get genome size for further computation.

In **example_input.tsv**, we have 2 samples to check. One is CARCR (Cariama cristata), another is HARAX (Harmonia axyridis). For CARCR, the BIOPROJECT  is [PRJNA212889](https://www.ebi.ac.uk/ena/browser/view/PRJNA212889?show=reads), the ASSEMBLY is [GCA_000690535.1](https://www.ncbi.nlm.nih.gov/assembly/GCA_000690535.1) (GCF_000690535.1 also works). 

## output files

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

# Local usuage (Who have local reads, do not want to use public data)
## command line
Users need to understand the structure of ***TRIP***. Read **TRIP structure** to understand.

Firstly, run `module4.py`
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

Then, run `module5.py`
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

Finally, run `module6.py`
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

# TRIP structure
```
## module 1
Given the NAME column and output_dir, check whether name-folder exists (delete if exists),
otherwise, create it. Create processed_tables folder in working dir to store tables processed from
repeatmaster output. Create barplots folder to store 4 types of barplots generated
from proccessed tables. Create filtered_tables to store filtered tables from
processed tables. Create manual.txt to record failed NAMEs for further manual
procession.

for each thread:
    ## module 2
    Given the BIOPROJECT, download the recording file from ENA database to the
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
and generate the TR_candidates folder to store TR candidates.

```
We suggest users to read original code when needed.

# Q&A
***Why my TRIP seems not to be running?***

At beginning, you may observe no running via `htop` or other background-check command, which is because TRIP is downloading files `tree path/to/TRIP_results to check`, the `wget` method built-in TRIP consumes neglectable computing resources.

***Can TRIP handle long sequencing reads?***

We haven't tested it. But we offer `--skip_subreads`, which will let ***TRIP*** skip reads names containing "subreads".
