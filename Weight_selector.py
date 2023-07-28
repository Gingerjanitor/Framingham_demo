# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 16:24:54 2023

@author: Matt0
"""
import numpy as np

def weight_selector(varname,Sex,age,treated):

    ###Classify them into the proper age group
    agecats=[(age>=30) & (age<=39),
             (age>=40) & (age<=49),
             (age>=50) & (age<=59),
             (age>=60) & (age<=69),
             (age>=70) & (age<=79)]
    
    ageflags=[0,1,2,3,4]
    agegroup=np.select(agecats,ageflags)
    
    
    
    ###based on the variable inputted, select the appropriate score weights
    if varname=='Age':
        Age_wgts={'M':[-9,-4,0,3,6,8,10,11,12,13],
                  'F':[-7,-3,0,3,6,8,10,12,14,16]}
        wgtset=Age_wgts[Sex]
        print(wgtset)
        return wgtset
    
    if varname=="Cholest":
    
        Cholest_wgts={'M':[[0,4,7,9,11],
                           [0,3,5,6,8],
                           [0,2,3,4,5],
                           [0,1,1,2,3],
                           [0,0,0,1,1]],
                      
                      'F':[[0,4,8,11,13],
                           [0,3,6,8,10],
                           [0,2,4,5,7],
                           [0,1,2,3,4],
                           [0,1,1,2,2]]}
        wgtset=Cholest_wgts[Sex][agegroup]
        print(wgtset)
        return wgtset
    
    if varname=="Smoke":
    
        Smoke_wgts={'M':[[0,8],
                        [0,5],
                        [0,3],
                        [0,1],
                        [0,1]],
                   'F':[[0,9],
                        [0,7],
                        [0,4],
                        [0,2],
                        [0,1]]}
        wgtset=Smoke_wgts[Sex][agegroup]
        print(wgtset)
        #return wgtset
    
    if varname=="Systolic":
        Systolic_wgts={"Treated":[0,1,2,3,4],
                 "Untreated":[0,3,4,5,6]}
        wgtset=Systolic_wgts[treated]
        #return wgtset
    
    
    
    
    
