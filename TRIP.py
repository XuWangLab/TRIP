#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 09:45:30 2020

@author: 23712

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 1
Given the NAME column and output_dir, check whether name-folder exists (delete if exists),
otherwise, create it. Copy the input tsv file into working dir as TRIP log. Create
processed_tables folder in working dir to store processed tables processed from
repeatmaster output. Create barplots folder to store 4 types of barplots generated
from proccessed tables. Create filtered_tables to store filtered tables from 
processed tables. Create manual.txt to record failed NAMEs for further manual
procession.

for each thread:
    ## module 2
    Given the BIOPROJECT, download the recording file from ENA database to the 
    name-folder. Then use parsing script to extract FASTQ file FTP locations. 
    Download the FASTQ files to the name-folder. Add FTP column to the log.
    ## module 3 
    Given the ASSEMBLY, web-scrap the "Total ungapped length" from NCBI website
    and add GENOME_SIZE to the log.
    ## module 4
    Given the dir to repeatmaster (come with TRIP), process the FASTQ files in name-folder
    and generate intermediates into name-folder.
    ## module 5
    Process the repeatmaster output tables and store into processed_tables.

## module 6
Given the filtration parameters to filter the processed tables in processed_tables
and generate the TR_candidates table and TR_candidates.dominant table.

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

####=======================================================================####
"""
from module_1 import module1
import os
import sys
import pandas as pd

infile_dir=r"C:\CurrentProjects\Telomere\code\TRIP\TRIP_input.tsv"
output_dir=r"C:\CurrentProjects\Telomere\code\TRIP"

## read infile
try:
    infile_df=pd.read_csv(infile_dir,header=0,sep="\t")
except Exception as e:
    print("error: The input tsv file has issues.")
    print(e)
    sys.exit()

## get the list of NAMEs
name_list=list(infile_df.loc[:,'NAME'])

## pass the infile_dir,name_list, output_dir, to module1
module1(infile_dir,output_dir,name_list)

