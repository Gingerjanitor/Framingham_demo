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

#gen new data
Patients['tempcost']=np.random.randint(85,7000, len(Patients['Framingham']))
Patients['Annual_med_costs']=(Patients['Framingham']+.003*Patients['tempcost'])*100
del Patients['tempcost']

###compute risk tiers

Patients=pd.concat([Patients,risk.risk_assign(Patients['Framingham'],Patients['Gender'])],axis=1)


#sns.set(font_scale=1.2)

#let's return to this, but when the risk indicators are factored in.


hue=Patients['Annual_med_costs']
sns.set_theme()
#sns.set_style("dark")
sns.scatterplot(Patients,x='Framingham',y='Annual_med_costs',hue=hue, palette=("rocket"))
plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
plt.xlabel("Framingham score", fontsize=15)
plt.ylabel("Annual medical expenditures", fontsize=15)
plt.legend("Risk tier",    )
