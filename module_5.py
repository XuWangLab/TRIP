#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:03:57 2021

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 5
Process the repeatmaster output tables and store into processed_tables.

CRPG_input.tsv:
code,read_len,num_reads,avg_genome_cov,genome_size
SUSSC,151,693665606,42.36,2472461935
#================================== input =====================================

#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================
python3  current_script_dir/module_5.py CRPG_loc name name_folder_dir
## Cal_Repeats_Per_Genome_and_Percent_of_Len_Linux.py will automatically find 
## the name_repeatsummary.tsv file in the name_folder_dir given the CRPG_input_df.tsv
python3 Cal_Repeats_Per_Genome_and_Percent_of_Len_Linux.py name_folder_dir CRPG_input_df.tsv output_tables output_figs
#================================== warning ===================================

####=======================================================================####
"""
import sys
import os
import pandas as pd

CRPG_loc=sys.argv[1]
name=sys.argv[2]
name_folder_dir=sys.argv[3]
output_dir=sys.argv[4]

## prepare the CRPG_input.tsv for Cal_Repeats_Per_Genome_and_Percent_of_Len_Linux.py
"""
cat name.stat ## generated by repeatmaster
reads	7008213708
bases	707829584508
"""
## read_len=bases/reads
## genome_size was stored in genome_size file
## avg_genome_cov=bases/genome_size
stat_file=str(name_folder_dir+"/"+name+".stat")
stat_df=pd.read_csv(stat_file,header=None,sep="\t")
reads_num=stat_df.loc[0,1]
bases_num=stat_df.loc[1,1]
read_len=float('%.2f' % bases_num/reads_num )

with open("genome_size",'r') as f:
    genome_size=int(f.readline())

avg_genome_cov=float('%.2f' % bases_num/genome_size)

CRPG_input_dict={'code':[name],
                 'read_len':[read_len],
                 'num_reads':[reads_num],
                 'avg_genome_cov':[avg_genome_cov],
                 'genome_size':[genome_size]
                 }

CRPG_input_df=pd.DataFrame.from_dict(CRPG_input_dict)
## write CRPG_input.tsv
CRPG_input_df.to_csv("CRPG_input.tsv",sep="\t",index=None)
CRPG_input_loc=str(name_folder_dir+"/"+"CRPG_input.tsv")


## parse the CRPG_input.tsv to Cal_Repeats_Per_Genome_and_Percent_of_Len_Linux.py
filtered_tables_dir=str(output_dir+"/"+"filtered_tables")
barplots_dir=str(output_dir+"/"+"barplots")
CRPG_cmd=str('python3 '+CRPG_loc+" "+name_folder_dir+" "+CRPG_input_loc+" "+filtered_tables_dir+" "+barplots_dir)
os.system(CRPG_cmd)
