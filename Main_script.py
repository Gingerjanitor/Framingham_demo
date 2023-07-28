# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:04:50 2023

@author: Matt0
"""
import Scorers as scorer
import pandas as pd
import numpy as np
import Weight_selector as weight_selector
#import Scorers as scorer
#Framingham tinker
#Framingham Risk Score 

Patients=pd.read_csv(r"C:\Users\Matt0\test project\Scratch and study files\Framingham practice.txt").rename(
    columns={'Total_Cholesterol':'Cholest','HDL_Cholesterol':'HDL',
             'Smoking_Status':'Smoke', 'Systolic_Blood_Pressure':'Systolic',
             'Treatment_for_High_BP':'Treat'})



#purge missings if any
Patients.dropna()
rawscores=pd.DataFrame()
rawscores['age_scr']=scorer.age_scorer(Patients)
rawscores['cholest_scr']=scorer.cholest_scorer(Patients)
rawscores['hdl_scr']=scorer.hdl_scorer(Patients)

rawscores['smoke_scr']=scorer.smoke_scorer(Patients)
rawscores['systol_scr']=scorer.systolic_scorer(Patients)

Patients['Framingham']=rawscores.sum(axis=1)
