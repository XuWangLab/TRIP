#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 14:45:48 2021

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####
## module 4
Given the dir to repeatmaster (come with TRIP), process the FASTQ files in name-folder
and generate intermediates into name-folder.
#================================== input =====================================

#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================
RepeatDetector  name_out  name/*gz  -r 1 -R 25 -n 24
RepeatSummary name_25nt.tsv name_out.repeat
#================================== warning ===================================

####=======================================================================####
"""
import sys
import os
import pandas as pd

RepeatDetector_loc=sys.argv[1]
RepeatSummary_loc=sys.argv[2]
RepeatDetector_O=sys.argv[3]
RepeatDetector_r=sys.argv[4]
RepeatDetector_R=sys.argv[5]
RepeatDetector_n=sys.argv[6]
RepeatDetector_I=sys.argv[7]
RepeatSummary_O=sys.argv[8]
RepeatSummary_I=sys.argv[9]


RepeatDetector_cmd=str(RepeatDetector_loc+" "+RepeatDetector_O+" "+RepeatDetector_I\
                       +" -r "+RepeatDetector_r+" -R "+RepeatDetector_R+" -n "+\
                       RepeatDetector_n)
os.system(RepeatDetector_cmd)

RepeatSummary_cmd=str(RepeatSummary_loc+" "+RepeatSummary_O+" "+RepeatSummary_I)
os.system(RepeatSummary_cmd)
