#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:10:17 2020

@author: Yihang Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ description ==============================####

#================================== input =====================================

#================================== output ====================================

#================================ parameters ==================================

#================================== example ===================================

#================================== warning ===================================

####=======================================================================####
"""
import os
import inspect

my_pos=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print("my position: ",my_pos)
cmd=str("python3 " + my_pos+"/untitled2.py")
os.system(cmd)

