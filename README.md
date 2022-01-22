# TRIP
***TRIP*** is a pipeline for identifying the TRM in NGS short reads (DNA). TRIP is ultra-fast, easy-to-use, and accurate. During our test in more than 100 species, ***TRIP*** successfully identified several unexpected novel TRM, with no false-positive case. For species which has no TRM (Dipteran, etc), ***TRIP*** smartly will identify 0 TRM candidates. 

# Installation
0. **Pre-needed** 
- Linux system (not supporting Windows.)
- **weget, python3, bash, tail, cat, rm** commands should be able to be called.
- **matplotlib, multiprocessing** package should be installed in python3.

1. Download the code and store the code folder in someplace. ***Do not change the content in the folder***.

# Basic usage (auto web-crawling > downloading > analyzing > filtering > output plots and tables)
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

***TRIP*** will parse the input file (make sure your input file is the same format as example_input.tsv). Each row in input file is a sample. 
The **NAME** column should be unique.
The **BIOPROJECT** column should be correct. The definition of **BIOPROJECT** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/bioproject/).
