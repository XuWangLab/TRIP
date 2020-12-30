#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 13:15:45 2020

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 2
Given the BIOPROJECT, download the recording file from ENA database to the 
name-folder. Then use parsing script to extract FASTQ file FTP locations. 
Download the FASTQ files to the name-folder.
#================================== input =====================================

#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================
python3 current_script_dir/module_2.py name prj name_folder_dir ENA2URL_loc wget_loc
#================================== warning ===================================

####=======================================================================####
"""
import sys
import os
import pandas as pd

name=sys.argv[1]
prj=sys.argv[2]
name_folder_dir=sys.argv[3]
ENA2URL_loc=sys.argv[4]
wget_loc=sys.argv[5]

## download records from ENA
ENA_record=str(name+"_"+prj+"_tsv.txt")
url=str("\"https://www.ebi.ac.uk/ena/portal/api/filereport?accession="+prj+"&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true\"")
wget_cmd=str("wget "+url+" -O "+name_folder_dir+"/"+ENA_record)
os.system(wget_cmd)


## parse the FTP locations
cp_cmd=str("cp -t "+name_folder_dir+" "+ENA2URL_loc+" "+wget_loc)
os.system(cp_cmd)
## will generate url file under name-folder
parse_cmd=str("bash "+name_folder_dir+"/ENA2URL.sh")
os.system(parse_cmd)

## Download the FASTQ files to the name-folder
wget_cmd=str("bash "+name_folder_dir+"/wget.sh")
os.system(wget_cmd)


