# TRIP
***TRIP*** is a pipeline for identifying the TRM in NGS short reads (DNA). TRIP is ultra-fast, easy-to-use, and accurate. During our test in more than 100 species, ***TRIP*** successfully identified several unexpected novel TRM, all known TRM, with no false-positive case. For species which has no TRM (Dipteran, etc), ***TRIP*** smartly will identify 0 TRM candidates.

***TRIP*** is designed to be able to take advantage of all public data. Therefore, the basic usage of ***TRIP*** is just to provide a table, using default parameters, set a ***LARGE*** `--process_num` (the calculation of ***TRIP*** is very small, the bottleneck is actually the downloading speed from NCBI/ENA database), run it in background, and enjoy the rest of your life. To make life easier, ***TRIP*** also set `--continue True` as default, so you don't have to worry about any failure. Since most public data is huge, you can use `--downsample` to limit diskusage.

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

# Basic usage (auto web-crawling > downloading > analyzing > filtering > output plots and tables)
> python3 path/to/TRIP/TRIP.py --input path/to/TRIP/example_input.tsv --output ./ --process_num 100

***TRIP*** will parse the input file (make sure your input file is the same format as example_input.tsv). Each row in input file is a sample. 
The **NAME** column should be unique.
The **BIOPROJECT** column should be correct. The definition of **BIOPROJECT** can be found in [NCBI](https://www.ncbi.nlm.nih.gov/bioproject/).
