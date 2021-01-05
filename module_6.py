#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:01:06 2021

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 6
Given the filtration parameters to filter the processed tables in processed_tables
and generate the TR_candidates table and TR_candidates.dominant table. Add FTP column to the log.
Add GENOME_SIZE to the log.
#================================== input =====================================

#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================

#================================== warning ===================================

####=======================================================================####
"""
import sys
import os

filtered_tables_dir=sys.argv[1]
rpt_reads_num=sys.argv[1]
total_reads_num=sys.argv[1]
repeats_num=sys.argv[1]
total_bases_num=sys.argv[1]
unit_len=sys.argv[1]
eff_read_len=sys.argv[1]
genome_size=sys.argv[1]
avg_genome_cov=sys.argv[1]
repeats_total_len=sys.argv[1]
repeats_per_read=sys.argv[1]
reads_per_genome=sys.argv[1]
repeats_per_genome=sys.argv[1]
repeats_per_million_reads=sys.argv[1]
repeats_len_per_genome=sys.argv[1]
repeats_len_per_million_reads=sys.argv[1]
percent_repeats_len_per_read=sys.argv[1]
percent_repeats_len_per_genome=sys.argv[1]
percent_repeat_unit_in_seqs=sys.argv[1]
best_candidate_enrichment=sys.argv[1]



