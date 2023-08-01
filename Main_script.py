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
from time import sleep
from openpyxl.workbook import workbook
from openpyxl import load_workbook

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

#gen new data

print("\n\n_____________________________________________\n\n")

Patients=analyze.gendata(Patients)

print("\n\n_____________________________________________\n\n")

analyze.show_risky(Patients)

print("\n\n_____________________________________________\n\n")


analyze.crosstab(Patients)



#################
      
###make a couple histograms 

print("\n\n_____________________________________________\n\n")

###press enter to continue###

analyze.makehistogram(Patients)
        
print("\n\n_____________________________________________\n\n")

analyze.runscatter(Patients)
##Mixing in gender






        
    if showchi.lower()=="y":



sns.regplot(x = "Risk_pct", y = "Annual_med_costs", data = Patients)
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("10-year risk %", fontsize=15)
plt.ylabel("Annual medical expenditures", fontsize=15)
plt.legend(["Female","Male"])
          
          
          
          
          
          
          
      The coloring of the dots highlights substantial gender differences in the Framingham scores, with men \
      having a mean of {means['M'].round(1)} versus a mean of {means['F'].round(1)} for women \n. At first \
      blush this is confusing, as authors such as Park and Pepine (2015) point out research that highlights that these data underestimate  \
      women's risk of heart attacks. But this is because we're looking at the raw scores, not the corresponding 10-year risks. The calibration of \
      the scores is such that women can earn much higher scores then men, but their risk is usually still lower. \n \n \
     'to prove this to ourselves, we can plot them against each other and see that men have considerably higher 10-year \
      risk despite lower framingham scores \n \n. ")
          
Print("All this indicates that we really need to control for sex in a final analysis!'")
      
hue=Patients['Genderdum']
sns.set_theme()
#sns.set_style("dark")
sns.scatterplot(Patients,x='Risk_pct',y='Annual_med_costs',hue=hue, palette=("rocket"))
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("10-year risk %", fontsize=15)
plt.ylabel("Annual medical expenditures", fontsize=15)
plt.legend(["Female","Male"])

hue=Patients['Genderdum']
sns.set_theme()
#sns.set_style("dark")
sns.scatterplot(Patients,x='Risk_pct',y='Annual_med_costs',hue=hue, palette=("rocket"))
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("10-year risk %", fontsize=15)
plt.ylabel("Annual medical expenditures", fontsize=15)
plt.legend(["Female","Male"])

##################

hue=Patients['Highrisknum']
sns.set_theme()
#sns.set_style("dark")
sns.scatterplot(Patients,x='Framingham',y='Annual_med_costs',hue=hue, palette=("rocket"))
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("Framingham score", fontsize=15)
plt.ylabel("Annual medical expenditures", fontsize=15)
plt.legend(["<15% risk","High risk"])

