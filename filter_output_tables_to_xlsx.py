#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 22:56:01 2020

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
#
#================================== input =====================================
#
#================================== output ====================================
#
#================================ parameters ==================================
#
#================================== example ===================================
#
#================================== warning ===================================
#
####=======================================================================####
"""

import pandas as pd
import os
import traceback
import sys

processed_output=sys.argv[1]
processed_output=r"C:\CurrentProjects\Telomere\2020_telomere_publication_self\Data_S7_TRIP_upstream_output_tables"
processed_tables=processed_output.rstrip("/").rstrip("\\")
table_names=os.listdir(processed_output)


## folder for .xlsx format tables with availability to filter
outputfolder="TR_candidates_5"
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)

## set up rules.
## rules are based on column names defined in previous python script.
def filter_out_low_quality_candidates(df,rpt_reads_num_filter,\
total_reads_num_filter,repeats_num_filter,total_bases_num,unit_len_filter,eff_read_len,genome_size_filter,\
avg_genome_cov_filter,repeats_total_len_filter,repeats_per_read_filter,reads_per_genome_filter,repeats_per_genome_filter,\
repeats_per_million_reads_filter,repeats_len_per_genome_filter,repeats_len_per_million_reads_filter,\
percent_repeats_len_per_read_filter,percent_repeats_len_per_genome_filter,\
percent_repeat_unit_in_seqs_filter):
    
    ## data quality guarantee 
    avg_genome_cov=df["avg_genome_cov"].to_numpy()
    repeat_containing_reads_num=df["reads"].to_numpy()

    ## telomere objective law
    ## 1. make sure we sequenced telomere region
    repeats_len_per_million_reads=df["repeats_len_per_million_reads"].to_numpy()
    ## 2. make sure the reads mapped to the real continuous telomere region
    ## exclude the unknown nosiy sparse/discrete repeats region
    percent_repeats_len_per_read=df["percent_repeats_len_per_read"].to_numpy()
    ## 3. TR unit length less than 5bp are excluded
    unit_len=df["unit_len"].to_numpy()
    ## 4. exclude 2bp repeats, such as AG, repeats region noise
    #repeats_per_read=df["repeats_per_read"].to_numpy()
    
    ## only accpet situations which no more than 2 TR candidates appeared at 
    ## the same time. if there are qualified TR candidates, we can not sure 
    ## it is not due to retrotransposon, sequencing errors or other situations.
    ## in order to distinguish the 2 TR candidates, we objectively use
    ## repeats_total_length. The dominant one must exceed 10 times than the 
    ## following one as for repeats_total_length. Otherwise, both of them will
    ## be excluded.
    repeats_total_len=df['repeats_total_len'].to_numpy()

    #repeat_containing_reads_per_genome
    repeat_containing_reads_filter=[1 if x>rpt_reads_num else 0 for x in repeat_containing_reads_num ] ## 12000
    avg_genome_cov_filter=[1 if x>10 else 0 for x in avg_genome_cov] ## 10
    
    
    ## repeats_len is kb
    repeats_len_per_million_reads_filter=[1 if x > 4 else 0 for x in repeats_len_per_million_reads]
    percent_repeats_len_per_read_filter=[1 if x > 0.5 else 0 for x in percent_repeats_len_per_read]
    unit_len_filter=[1 if x>4 else 0 for x in unit_len ]
    #repeats_per_read_filter=[1 if x> 10 else 0 for x in repeats_per_read]
    
    
    """
    repeats_per_genome_filter=[1 if x>500 else 0 for x in repeats_per_genome ] ## or 1000
    repeat_containing_reads_num_filter=[1 if x > 10000 else 0 for x in repeat_containing_reads_num] ## test
    reads_per_genome_filter=[1 if x>100 else 0 for x in reads_per_genome]
    """

    sum_scores=[sum(i) for i in zip(
        avg_genome_cov_filter,\
        repeat_containing_reads_filter,\
        repeats_len_per_million_reads_filter,\
        unit_len_filter,\
        percent_repeats_len_per_read_filter,\
        #repeats_per_read_filter
                )]
    ##print(sum_scores)
    qualified=[1 if x==5 else 0 for x in sum_scores]

    return  avg_genome_cov_filter,\
            repeat_containing_reads_filter,\
            repeats_len_per_million_reads_filter,\
            unit_len_filter,\
            repeats_total_len,\
            percent_repeats_len_per_read_filter,\
            qualified
            #repeats_per_read_filter,\

## all possible condidates
## if there're more than 1 candidates, which is ambiguous
TR_candidates_qualified_df_sum=pd.DataFrame()
TR_candidates_qualified_dominant=pd.DataFrame()

for name in table_names:
    print(name)
    if "csv" in name or "tsv" in name: ## filter unexpected files
        processed_table="/".join([processed_output,name])
        processed_table_df=pd.read_csv(processed_table)
        try:
            avg_genome_cov_filter,\
            repeat_containing_reads_filter,\
            repeats_len_per_million_reads_filter,\
            unit_len_filter,\
            repeats_total_len,\
            percent_repeats_len_per_read_filter,\
            qualified=filter_out_low_quality_candidates(processed_table_df)
            #repeats_per_read_filter,\
        except :
            print(name," has problem:")
            traceback.print_exc()
            continue

        filter_results=pd.DataFrame({
               'avg_genome_cov_filter':avg_genome_cov_filter,\
               'repeat_containing_reads_filter':repeat_containing_reads_filter,\
               'repeats_len_per_million_reads_filter':repeats_len_per_million_reads_filter,\
               'unit_len_filter':unit_len_filter,\
               'percent_repeats_len_per_read_filter':percent_repeats_len_per_read_filter,\
               'qualified':qualified
                })
               #'repeats_per_read_filter':repeats_per_read_filter,\

        TR_candidates_df=pd.concat([processed_table_df,filter_results],axis=1)

        TR_candidates_qualified_df=TR_candidates_df[TR_candidates_df['qualified']==1]
        TR_candidates_qualified_num=TR_candidates_qualified_df.shape[0]
        TR_candidates_qualified_df.index=range(TR_candidates_qualified_num)
        
        ## TR_candidates_qualified_df need to be formatted to output TR_candidates_qualified_df_sum
        TR_candidates_qualified_df.loc[:,'species']=[name]*TR_candidates_qualified_num
        TR_candidates_qualified_df.loc[:,'qualified_num']=[TR_candidates_qualified_num]*TR_candidates_qualified_num
        TR_candidates_qualified_df_sum=pd.concat([TR_candidates_qualified_df_sum,TR_candidates_qualified_df],axis=0)
        
        ## TR_candidates_df need to be formatted to output TR_candidates_qualified_dominant
        TR_candidates_df.to_excel(str(outputfolder+"/"+name+"."+str(TR_candidates_qualified_num)+".filtered.xlsx"),index=None)
        
        ## there cannot be to many qualified TR candidates, otherwise it will be too noisy
        max_qualified_num=999

        ## the TR candidate should satisfy two conditions
        ## one, is qualified (pass all above filters)
        ## two, is dominant (repeats_total_len is more than ${difference_threold} times than the follower)
        difference_threhold=3
        if max_qualified_num>=TR_candidates_qualified_num>0:
            ## the TR candidate must extremly more doinant than the followers
            ## so set the repeats_len_per_million_reads difference to 5 times
            sorted_TR_qualified_candidates_df=\
            TR_candidates_qualified_df.sort_values("repeats_total_len",ascending=False,inplace=False)
            sorted_TR_qualified_candidates_df.index=range(sorted_TR_qualified_candidates_df.shape[0])
            count=0
            
            if TR_candidates_qualified_num==1:
                dominant_TR_candidate=pd.DataFrame(sorted_TR_qualified_candidates_df.loc[0]).T
                dominant_TR_candidate.loc[:,'difference']=1
                TR_candidates_qualified_dominant=pd.concat([TR_candidates_qualified_dominant,dominant_TR_candidate],axis=0)
                
                print(name," : only dominant")                
                
            elif TR_candidates_qualified_num>1:
                dominant=1
                first_repeats_total_len=sorted_TR_qualified_candidates_df.loc[0,'repeats_total_len']
                second_repeats_total_len=sorted_TR_qualified_candidates_df.loc[1,'repeats_total_len']
                difference=first_repeats_total_len/second_repeats_total_len
                
                print(name," : ",difference)
                      
                if difference>difference_threhold:
                    dominant=1
                    dominant_TR_candidate=pd.DataFrame(sorted_TR_qualified_candidates_df.loc[0]).T
                    dominant_TR_candidate.loc[:,'difference']=difference
                    TR_candidates_qualified_dominant=pd.concat([TR_candidates_qualified_dominant,dominant_TR_candidate],axis=0)

        else:
            print(name," has no qualified TR candidate, or there're too many of them.")
            continue


    else:
        continue

TR_candidates_qualified_df_sum.to_excel(str(outputfolder+"/"+outputfolder+".qualified.xlsx"),index=None)
TR_candidates_qualified_dominant.to_excel(str(outputfolder+"/"+outputfolder+".qualified.dominant.xlsx"),index=None)

