# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:04:50 2023

@author: Matt0
"""
import Scorers as scorer
import run_analyses as analyze
import pandas as pd
import Weight_selector as ws
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import Risk_assign as risk
from scipy.stats import chi2_contingency
from openpyxl.workbook import workbook
from openpyxl import load_workbook
import statsmodels.api as sm
from scipy import stats

from statsmodels.compat import lzip
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

sns.set_theme()



#import the data
Patients=pd.read_csv(r"C:\Users\Matt0\test project\Framingham score tool\Framingham practice more.txt").rename(
    columns={'Total_Cholesterol':'Cholest','HDL_Cholesterol':'HDL',
             'Smoking_Status':'Smoke', 'Systolic_Blood_Pressure':'Systolic',
             'Treatment_for_High_BP':'Treat'})
#purge missings if any
Patients.dropna()

#load the work book with the script
wb=load_workbook("C:/Users/Matt0/test project/Framingham score tool/Script.xlsx")


ws=wb.active
#Show the welcome message
#Make me a input later
print(ws["A2"].value)
print("\n\n\n") ###Delete me later after input implemented

print(ws["C2"].value)

print("\n\n_____________________________________________\n\n")

print(Patients.head(5))
input("\n\nPress enter to start calculating the Framingham scores")

rawscores=pd.DataFrame()
rawscores['age_scr']=scorer.age_scorer(Patients)
rawscores['cholest_scr']=scorer.cholest_scorer(Patients)
rawscores['hdl_scr']=scorer.hdl_scorer(Patients)

rawscores['smoke_scr']=scorer.smoke_scorer(Patients)
rawscores['systol_scr']=scorer.systolic_scorer(Patients)

Patients['Framingham']=rawscores.sum(axis=1)

print("\n\n_____________________________________________\n\n")

print(f"""{ws["C3"].value}\n\n""")

print(rawscores.head(5))

input("\n\nPress enter to continue")

print("\n\n_____________________________________________\n\n")
print("\n\n The rows are then combined and merged into the main dataset\n\n")
print(Patients.head(5))

input("\n\nPress enter to continue")

###compute risk tiers

Patients=pd.concat([Patients,risk.risk_assign(Patients['Framingham'],Patients['Gender'])],axis=1)

print("\n\n_____________________________________________\n\n")


print(f"""\n\n{ws["C4"].value}\n\n""")

print(Patients[['Gender', 'Framingham','Risk_pct','Riskcats','Highrisk']].head(5))

input("\n\nPress enter to continue")

#pd.DataFrame.to_csv(Patients,"almost prepared data")


#############

######################
#Run Some analysis   # 
######################

####Generate the fake data

print("\n\n_____________________________________________\n\n")

Patients=analyze.gendata(Patients)

####Show high risk patients

print("\n\n_____________________________________________\n\n")

analyze.show_risky(Patients)

print("\n\n_____________________________________________\n\n")

####Run a cross tabulation

analyze.crosstab(Patients)



#################
      

print("\n\n_____________________________________________\n\n")

###press enter to continue###
####Make a couple histograms

analyze.makehistogram(Patients)
        
print("\n\n_____________________________________________\n\n")
####Do the scatter plot
analyze.runscatter(Patients)



####Do the continuos model demo
analyze.OLSdemo(Patients)






