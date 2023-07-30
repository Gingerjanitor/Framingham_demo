# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:04:50 2023

@author: Matt0
"""
import Scorers as scorer
import pandas as pd
import Weight_selector as ws
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import Risk_assign as risk
#import Scorers as scorer
#Framingham tinker
#Framingham Risk Score 

Patients=pd.read_csv(r"C:\Users\Matt0\test project\Framingham score tool\Framingham practice more.txt").rename(
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

###compute risk tiers

Patients=pd.concat([Patients,risk.risk_assign(Patients['Framingham'],Patients['Gender'])],axis=1)

#pd.DataFrame.to_csv(Patients,"almost prepared data")




######################
#Run Some analysis   # 
######################

#gen new data
Patients['tempcost']=np.random.randint(85,7000, len(Patients['Framingham']))
#Impose a correlation between this new variable and Framingham scores
Patients['Annual_med_costs']=(Patients['Framingham']+.003*Patients['tempcost'])*100
del Patients['tempcost']

#dummy up gender for later
Patients["Genderdum"]=pd.get_dummies(Patients['Gender'],prefix='num',drop_first=True)

########STEP 1: Ask if they want to see high risk patients.
#Show if yes, move on if no
#
#get the IDs for people
atrisk=pd.DataFrame(Patients.loc[Patients['Highrisk']=='>20% risk','Patient_ID'])
atrisk=pd.merge(atrisk,Patients[['Patient_ID','Risk_pct']], on='Patient_ID')

##sns.histogram(Patients, x='Framingham')

showrisk=str(input(f"Let's put this data to work. \n\n There are {len(atrisk)} people in the dataset with over 20% risk. Perhaps we should notify their care team? Press Y to see their IDs, N to move on \n"))
while showrisk.lower() not in ['y','n']:
    showrisk=str(input("Please enter either Y or N \n"))

if showrisk.lower()=="y":

    center="The following patients IDs have above 20% estimated risk of coronary heart disease in the next decade. \n\n Below is each ID and risk % \n"
    center=center.center(45)
    print(center)
    for case in atrisk.itertuples():
        print(f'Patient ID: {case[1]}, risk of %{case[2]}')

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
      they were designed to be there. My interpretations of the statistics are just for \n\
      demonstration purposes.\n")


##press enter to continue###

print("First, it is important to examine distributions for both variables.")
pd.join()


sns.set_theme()


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

