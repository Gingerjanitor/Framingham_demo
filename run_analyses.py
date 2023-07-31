# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:17:10 2023

@author: Matt0
"""
import pandas as pd
import numpy as np
from openpyxl.workbook import workbook
from openpyxl import load_workbook
from scipy.stats import chi2_contingency


wb=load_workbook("C:/Users/Matt0/test project/Framingham score tool/Script.xlsx")
ws=wb.active

def gendata(Patients):
    np.random.seed(29293)
    Patients['tempcost']=np.random.randint(85,7000, 200)
    #Impose a correlation between this new variable and Framingham scores
    Patients['Annual_med_costs']=(Patients['Framingham']+.003*Patients['tempcost'])*100
    del Patients['tempcost']

    #dummy up gender for later
    Patients["Genderdum"]=pd.get_dummies(Patients['Gender'],prefix='num',drop_first=True)

    #An indicator of if they are a snap recipient or not
    Patients['SNAP']=np.random.default_rng().choice(["no","yes"],len(Patients['Gender']))
    #doctor it so Patients is correlated with high risk by randomly assigning some of the snap people to be high risk.
    rand=np.random.randint(0,100,200)
    Patients.loc[(rand>=35) & (Patients['Highrisk']==">20% risk"), 'SNAP']="yes"
    
    return Patients


def show_risky(Patients):
    ########STEP 1: Ask if they want to see high risk patients.
    #Show if yes, move on if no
    #
    #get the IDs for people
    atrisk=pd.DataFrame(Patients.loc[Patients['Highrisk']=='>20% risk','Patient_ID'])
    atrisk=pd.merge(atrisk,Patients[['Patient_ID','Risk_pct']], on='Patient_ID')
    
    ##sns.histogram(Patients, x='Framingham')
    text=ws['E2'].value
    text= text.replace("{len(atrisk)}",f'{len(atrisk)}')
    showrisk=input(text)
    while showrisk.lower() not in ['y','n']:
        showrisk=str(input("Please enter either Y or N \n"))
    
    if showrisk.lower()=="y":
        print("\n\n_____________________________________________\n\n")
        header="The following patients IDs have above 20% estimated risk of coronary heart disease in the next decade. \n\n Below is each ID and risk % \n"
        header=header.center(45)
        print(header)
        for case in atrisk.itertuples():
            print(f'Patient ID: {case[1]}, risk of {case[2]}%')

def crosstab(Patients):
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

    
    explain=str(input("\n Shall I provide an interpretation of these results and next steps? Y or N?\n"))
    while explain.lower() not in ['y','n']:
        
        explain=str(input("Please enter either Y or N \n"))
    
    if explain.lower()=="y":
        print("\n\n_____________________________________________\n\n")
        print(ws['G3'].value)
