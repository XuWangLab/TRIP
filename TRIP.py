#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 09:45:30 2020

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 1
Given the NAME column and output_dir, check whether name-folder exists (delete if exists),
otherwise, create it. Copy the input tsv file into working dir as TRIP log. Create
processed_tables folder in working dir to store tables processed from
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
    Process the repeatmaster output tables and store into processed_tables.

## module 6
Given the filtration parameters to filter the processed tables in processed_tables
and generate the TR_candidates table and TR_candidates.dominant table. Add FTP column to the log.
Add GENOME_SIZE to the log.

#================================== input =====================================
1.input tsv file:
NAME	BIOPROJECT	ASSEMBLY
CHAVOC	PRJNA212867	GCA_000708025.2
ACACHL	PRJNA212877	GCA_000695815.1

2.path to repeatmaster

2.1 -r	minimal repeat size (default=1)
2.2 -R	maximal repeat size (default=25)
2.3 -n	minimal #repeats*size (default=24, to control false positives)

3.output dir
#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================

#================================== warning ===================================
system: Linux
The structure of the folder should not change.
"python3" should be abled to call by your system.
"pandas" package should be installed in python3.
####=======================================================================####
"""
import os
import sys
import pandas as pd
import inspect

infile_dir=r"C:\CurrentProjects\Telomere\code\TRIP\TRIP_input.tsv"
output_dir=r"C:\CurrentProjects\Telomere\code\TRIP"
RepeatDetector_O="name_out"
RepeatDetector_r=1
RepeatDetector_R=25
RepeatDetector_n=16
RepeatDetector_I="*gz"
RepeatSummary_O="name.tsv"
RepeatSummary_I="name_out.repeat"

current_script_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ENA2URL_loc=str(current_script_dir+"/ENA2URL.sh")
wget_loc=str(current_script_dir+"/wget.sh")
RepeatDetector_loc=str(current_script_dir+"/RepeatDetector_v2")
RepeatSummary_loc=str(current_script_dir+"/RepeatSummary_v2")

## read infile
try:
    infile_df=pd.read_csv(infile_dir,header=0,sep="\t")
except Exception as e:
    print("error: The input tsv file has issues.")
    print(e)
    sys.exit()

## get the list of BIOPROJECTs
name_list=list(infile_df.loc[:,'NAME'])
prj_list=list(infile_df.loc[:,'BIOPROJECT'])
ass_list=list(infile_df.loc[:,'ASSEMBLY'])
name_prj_ass_list=list(zip(name_list,prj_list,ass_list))


## module 1 command
module_1_cmd=str("python3 "+current_script_dir+"/module_1.py "+infile_dir+" "+output_dir)
os.system(module_1_cmd)

for name_prj_ass in name_prj_ass_list:
    name=name_prj_ass[0]
    prj=name_prj_ass[1]
    ass=name_prj_ass[2]
    name_folder_dir=str(output_dir+"/"+name)  ## created in module 1
    ## module 2 command
    module_2_cmd=str("python3 "+current_script_dir+"/module_2.py "+name+" "+\
                     prj+" "+name_folder_dir+" "+ENA2URL_loc+" "+wget_loc)
    os.system(module_2_cmd)
    ## module 3 command
    module_3_cmd=str("python3 "+current_script_dir+"/module_3.py "+ass+" "+name_folder_dir)
    os.system(module_3_cmd)
    ## module 4 command
    module_4_cmd=str("python3 "+current_script_dir+"/module_4.py "+RepeatDetector_loc\
                     +" "+RepeatSummary_loc+" "+RepeatDetector_O+" "+RepeatDetector_r\
                     +" "+RepeatDetector_R+" "+RepeatDetector_n+" "+RepeatDetector_I\
                     +" "+RepeatSummary_O+" "+RepeatSummary_I)
        