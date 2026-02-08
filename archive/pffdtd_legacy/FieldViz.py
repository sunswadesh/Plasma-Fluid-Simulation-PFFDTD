#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:57:50 2021
Read Density and other field values from the pffdtd code. Reads in the .fd file
@author: nasrineshraghi
"""

import numpy as np
    
with open("dipole.fd") as infile:
    for line in range(15):#infile:
        print(line)
        if line ==0:
            print (infile.readline())
        if line == 1:  # 
            tmp = infile.readline()
            x = tmp.split("\t")                       
            x = np.asarray(x,int)
        if line == 2:  # 
            tmp = infile.readline()
            y = tmp.split("\t")                       
            y = np.asarray(y,int)
        if line == 3:  # 
            tmp = infile.readline()
            z = tmp.split("\t")                       
            z = np.asarray(z,int)
        if line >3:
            tmp = infile.readline()
            t[line-4] = tmp[0]
