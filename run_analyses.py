# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:17:10 2023

@author: Matt0
"""
import pandas as pd
import numpy as np
from openpyxl.workbook import workbook
from openpyxl import load_workbook

wb=load_workbook("C:/Users/Matt0/test project/Framingham score tool/Script.xlsx")
ws=wb.active

def gendata(Patients):
    Patients['tempcost']=np.random.randint(85,7000, len(Patients['Framingham']))
    #Impose a correlation between this new variable and Framingham scores
    Patients['Annual_med_costs']=(Patients['Framingham']+.003*Patients['tempcost'])*100
    del Patients['tempcost']

    #dummy up gender for later
    Patients["Genderdum"]=pd.get_dummies(Patients['Gender'],prefix='num',drop_first=True)

    #An indicator of if they are a snap recipient or not
    Patients['SNAP']=np.random.default_rng().choice(["no","yes"],len(Patients['Gender']))
    #doctor it so Patients is correlated with high risk by randomly assigning some of the snap people to be high risk.
    rand=np.random.randint(0,100,len(Patients['SNAP']))
    Patients.loc[(rand>=50) & (Patients['Highrisk']==">20% risk"), 'SNAP']="yes"
    
    return Patients


def show_risky(Patients):
    
    
    ########STEP 1: Ask if they want to see high risk patients.
    #Show if yes, move on if no
    #
    #get the IDs for people
    atrisk=pd.DataFrame(Patients.loc[Patients['Highrisk']=='>20% risk','Patient_ID'])
    atrisk=pd.merge(atrisk,Patients[['Patient_ID','Risk_pct']], on='Patient_ID')
    
    ##sns.histogram(Patients, x='Framingham')
    
    showrisk=str(input(f"""{ws["E2"].value}"""))
    while showrisk.lower() not in ['y','n']:
        showrisk=str(input("Please enter either Y or N \n"))
    
    if showrisk.lower()=="y":
    
        center="The following patients IDs have above 20% estimated risk of coronary heart disease in the next decade. \n\n Below is each ID and risk % \n"
        center=center.center(45)
        print(center)
        for case in atrisk.itertuples():
            print(f'Patient ID: {case[1]}, risk of {case[2]}%')
        print('\n\n')
    
