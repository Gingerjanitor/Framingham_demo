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
print("\n\n\n\n\n") ###Delete me later after input implemented

print(ws["C2"].value)

print("\n\n_____________________________________________\n\n")
print("\n\n")
print(Patients.head(5))
print("\n\n")
input("\n\nPress enter to start calculating the Framingham scores")

rawscores=pd.DataFrame()
rawscores['age_scr']=scorer.age_scorer(Patients)
rawscores['cholest_scr']=scorer.cholest_scorer(Patients)
rawscores['hdl_scr']=scorer.hdl_scorer(Patients)

rawscores['smoke_scr']=scorer.smoke_scorer(Patients)
rawscores['systol_scr']=scorer.systolic_scorer(Patients)

Patients['Framingham']=rawscores.sum(axis=1)

print("\n\n_____________________________________________\n\n")


print(f"""\n\n{ws["C3"].value}\n\n""")
print(rawscores.head(5))

input("\n\nPress enter to continue")

print("\n\n_____________________________________________\n\n")
print("\n\n The rows are then combined and merged into the main dataset\n\n")
print(Patients.head(5))


###compute risk tiers

Patients=pd.concat([Patients,risk.risk_assign(Patients['Framingham'],Patients['Gender'])],axis=1)

print("\n\n_____________________________________________\n\n")


print(f"""\n\n{ws["C4"].value}\n\n""")

print(Patients[['Gender', 'Framingham','Risk_pct','Riskcats','Highrisk']].head(5))

#pd.DataFrame.to_csv(Patients,"almost prepared data")


#############

######################
#Run Some analysis   # 
######################

#gen new data

print("\n\n_____________________________________________\n\n")

Patients=analyze.gendata(Patients)

print("\n\n_____________________________________________\n\n")


print(f"""{ws["C3"].value}\n\n""")

analyze.show_risky(Patients)

print("\n\n_____________________________________________\n\n")


analyze.crosstab(Patients)



#################
      
########STEP 2: Show an analysis of heart risk scores and medical expenditures
###Ask if they want to...
#   see histograms of both variables (then ask, do you want an interpretation?)
#   See a scatter plot (then ask, do you want an interpretation?)
#...Do a t-test
#...Do a regression.



print("simple analysis of these data.\n  \
      Do Framingham risk scores correlated with annual medical expenditures? \n \n\
      NOTE: Please note that all these data are fabricated, any correlations are there because \n \
      they were designed to be there. My interpretations are technically accurate, but meaningless! \n")

###

### A cross tab and chi square:
    
showchi=input(ws['G2'].value)
while showchi.lower() not in ['y','n']:
    showchi=str(input("Please enter either Y or N \n"))

if showchi.lower()=="y":
    print("\n\n_____________________________________________\n\n")  
    print("Here's a cross tab of risk scores and SNAP values, calculating percentages along columns. \n\n")
    nopct=pd.crosstab(Patients['Highrisk'],Patients['SNAP'])
    chi, p, df, expected= chi2_contingency(nopct)
    tab=(pd.crosstab(Patients['Highrisk'],Patients['SNAP'],normalize='columns').round(4)*100)
    cramersv=np.sqrt((chi/len(Patients['SNAP']*(len(tab)-1))))
    print(tab)
    
    print(f"\nChi-Square= {chi.round(2)}, p= {p.round(3)}")
    print(f"Cramer's V= {cramersv.round(3)}")

    
    explain=str(input("\n Shall I provide an interpretation of these results? Y or N?\n"))
    while explain.lower() not in ['y','n']:
        explain=str(input("Please enter either Y or N \n"))
    
    if explain.lower()=="y":
        print(ws['G3'].value)

    

    

###
##press enter to continue###

print("First, it is important to examine distributions for both variables.")
pd.join()




plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
f, axes = plt.subplots(1, 2)

sns.histplot(Patients['Framingham'], 
             bins=15,
             ax=axes[0])
axes[0].set_xlabel("Risk Score")
axes[0].set_title("Framingham Score Distribution")
axes[0].axvline(x=Patients['Framingham'].mean(),color='red')
axes[0].axvline(x=Patients['Framingham'].median(),color='blue')

sns.histplot(Patients['Annual_med_costs'],
             bins=20,
             ax=axes[1])
axes[1].set_title("Annual Medical Costs Distribution")
axes[1].set_xlabel("$ Spent Per Year")
axes[1].axvline(x=Patients['Annual_med_costs'].mean(),color='red')
axes[1].axvline(x=Patients['Annual_med_costs'].median(),color='blue')

plt.show()

print(f"Both distributions are relatively normal, but the also pile at fairly high values. \
      The mean risk score is {Patients['Framingham'].mean().round(2)}, which is much higher than shown in the literature, \
      which usually finds that scores tend to pile on the low end. This would be of interest to stakeholders, \
      who might be able to provide clarifications on why scores are so high amongst the sampled group, or it may indicate \
      a problem in the data handling/collection process- is data being misentered or misclassified during warehousing? \
      \n \n \
      ...But for our purposes, let's assume that the data is valid and might be sourced a particularly high risk population \
      such as attendees at an monthly free clinic for low income and housing insecure persons." )


means=Patients['Framingham'].groupby(Patients['Gender']).mean()
print(f"A simple scatter plot helps to clarify the relationship between the two variables. Here we can see \
      a clear positive correlation between the two. As Framingham scores increases,  medical \
      expenditures increase fairly reliably, with a strong Pearson's R of {Patients['Framingham'].corr(Patients['Annual_med_costs']).round(2)}.\n \
      It is likely that this relationship is not unidirectional- being sick is not easy on your wallet, and stressing about money isn't \
      going to help that high blood pressure! \n \n \
          \
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
sns.scatterplot(Patients,x='Framingham',y='Annual_med_costs',hue=hue, palette=("rocket"))
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("Framingham score", fontsize=15)
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

