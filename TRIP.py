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
    Process the repeatmaster output tables and store processed tables into processed_tables.
    Store barplots into barplots folder.

## module 6
Given the filtration parameters to filter the processed tables in processed_tables
and generate the TR_candidates folder to store TR candidates.

Add URL column to the log.
Add GENOME_SIZE to the log.
Save TRIP.log.csv

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
needed python pacakges:
    os
    sys
    pandas
    inspect
    numpy
    matplotlib
    requests
    random
    bs4
    time
    traceback
    multiprocessing
####=======================================================================####
"""
import os
import sys
import pandas as pd
import inspect
import time
##from multiprocessing import Process
from multiprocessing import Pool

## infile_dir=r"C:\CurrentProjects\Telomere\code\TRIP\TRIP_input.tsv"
## output_dir=r"C:\CurrentProjects\Telomere\code\TRIP"

infile_dir=sys.argv[1]
output_dir=sys.argv[2]

current_script_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
## str to int
process_num=32
ENA2URL_loc=str(current_script_dir+"/ENA2URL.sh")
wget_loc=str(current_script_dir+"/wget.sh")
RepeatDetector_loc=str(current_script_dir+"/RepeatDetector_v2")
RepeatSummary_loc=str(current_script_dir+"/RepeatSummary_v2")
RepeatDetector_r=1
RepeatDetector_R=25
RepeatDetector_n=16
CRPG_loc=str(current_script_dir+"/cal_repeats_per_genome_and_percent_of_len_linux.py")
rpt_reads_num=12000
total_reads_num=0
repeats_num=0
unit_len=5
eff_read_len=0
genome_size=0
avg_genome_cov=10
repeats_len=0
repeats_per_read=0
reads_per_genome=0
repeats_per_genome=0
repeats_per_million_reads=0
repeats_len_per_genome=0
repeats_len_per_million_reads=4 ##Kb
percent_repeats_len_per_read=0.5
percent_repeats_len_per_genome=0
percent_repeat_unit_in_seqs=0
best_candidate_enrichment=3
max_qualified_num=999
FOT2X_loc=str(current_script_dir+"/filter_output_tables_to_xlsx.py")


if __name__=='__main__':
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
    name_num=len(name_list)
    
    ## module 1 command
    module_1_cmd=str("python3 "+current_script_dir+"/module_1.py "+infile_dir+" "+output_dir)
    print("module 1: ",module_1_cmd)
    os.system(module_1_cmd)
    def module2to4(name,prj,ass):
        name_folder_dir=str(output_dir+"/TRIP_results/"+name)  ## created in module 1
        ## module 2 command
        module_2_cmd=str("python3 "+current_script_dir+"/module_2.py "+name+" "+\
                         prj+" "+name_folder_dir+" "+ENA2URL_loc+" "+wget_loc)
        print("module 2: ",module_2_cmd)
        os.system(module_2_cmd)
        ## module 3 command
        module_3_cmd=str("python3 "+current_script_dir+"/module_3.py "+ass+" "+name_folder_dir)
        print("module 3: ",module_3_cmd)
        os.system(module_3_cmd)
        ## module 4 command
        RepeatDetector_O="name_out"
        RepeatDetector_I="*gz"
        RepeatSummary_O="name_repeatsummary.tsv"
        RepeatSummary_I="name_out.repeat"
        module_4_cmd=str("python3 "+current_script_dir+"/module_4.py "+RepeatDetector_loc\
                         +" "+RepeatSummary_loc+" "+RepeatDetector_O+" "+RepeatDetector_r\
                         +" "+RepeatDetector_R+" "+RepeatDetector_n+" "+RepeatDetector_I\
                         +" "+RepeatSummary_O+" "+RepeatSummary_I)
        print("module 4: ",module_4_cmd)
        os.system(module_4_cmd)
        ## module 5 command
        module_5_cmd=str("python3 "+current_script_dir+"/module_5.py "+CRPG_loc+" "+name+" "+name_folder_dir+" "+output_dir)
        print("module 5: ",module_5_cmd)
        os.system(module_5_cmd)
    
    ## multi-process
    pool=Pool(process_num)

    for name_prj_ass in name_prj_ass_list:
        name=name_prj_ass[0]
        prj=name_prj_ass[1]
        ass=name_prj_ass[2]
        print("%s-%s-%s is processing." % (name,prj,ass))
        time.sleep(10)
        pool.apply_async(func=module2to4, args=(name,prj,ass,))

    pool.close()
    time.sleep(5)
    pool.join()
    
    ## module 6 command
    filtered_tables_dir=str(output_dir+"/TRIP_results/"+"filtered_tables")
    TR_candidates_dir=str(output_dir+"/TRIP_results/"+"TR_candidates")
    module_6_cmd=str("python3 "+current_script_dir+"/module_6.py "+filtered_tables_dir+" "+\
                    rpt_reads_num+" "+\
                    total_reads_num+" "+\
                    repeats_num+" "+\
                    unit_len+" "+\
                    eff_read_len+" "+\
                    genome_size+" "+\
                    avg_genome_cov+" "+\
                    repeats_len+" "+\
                    repeats_per_read+" "+\
                    reads_per_genome+" "+\
                    repeats_per_genome+" "+\
                    repeats_per_million_reads+" "+\
                    repeats_len_per_genome+" "+\
                    repeats_len_per_million_reads+" "+\
                    percent_repeats_len_per_read+" "+\
                    percent_repeats_len_per_genome+" "+\
                    percent_repeat_unit_in_seqs+" "+\
                    best_candidate_enrichment+" "+\
                    max_qualified_num+" "+\
                    TR_candidates_dir+" "+\
                    FOT2X_loc)
    print("module 6 is processing.")
    ## Add URL column to the log.
    ## Add GENOME_SIZE to the log.
    URL_list=[]
    GENOME_SIZE_list=[]
    for name in name_list:
        url_loc=str(output_dir+"/"+name+"/url")
        GENOME_SIZE_loc=str(output_dir+"/"+name+"/genome_size")
        with open(url_loc,'r') as f:
            lines=[x.strip() for x in f.readlines()]
            URL=";".join(lines)
            URL_list.append(URL)
        with open(GENOME_SIZE_loc,'r') as f:
            GENOME_SIZE=int(f.readline())
            GENOME_SIZE_list.append(GENOME_SIZE)
    
    infile_df['URL']=URL_list
    infile_df['GENOME_SIZE']=GENOME_SIZE
    
    infile_df.to_csv(str(output_dir+"/TRIP_results/"+"TRIP.log.csv"),index=None)
    
