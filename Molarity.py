#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:14:19 2024

@author: harshjain
"""

#%% How to make 10% DOPS Solution

Chemicals = ['DOPS','DOPC','LissRhod-PE', 'DOTAP']
Molecular_Weights = [809.518,785.593,1300.712,697.578]
#Exact masses extracted from Avanti-Lipids Website
Concentrations = [2.5,2.5,0.01,2.5]; # In chloroform

# https://avantilipids.com/product/840035
# https://avantilipids.com/product/850375
# https://avantilipids.com/product/810150
# https://avantilipids.com/product/890890


# DOPC is 2.5 mg/ml, DOPS is 2.5 mg/ml, LissRhod is 10ug/ml, 


#%% Let's make 10% charged DOPS-DOPC (Negative, Fluoroscent)
MixtureVolumes = [40,400,100,0];

#%% Let's make 10% charged DOTAP-DOPC (Positive, non-fluoroscent)
MixtureVolumes = [0,400,0,40];

