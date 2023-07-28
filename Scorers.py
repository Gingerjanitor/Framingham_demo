# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:43:14 2023

@author: Matt0

#This file establishes the functions that are used to convert raw patient data to scored data
"""
import pandas as pd
import numpy as np

#Scoring sheet can be found here https://onlinelibrary-wiley-com.ezproxy.clarkson.edu/doi/pdf/10.1002/sim.1742

######
######The scoring criteria are different based on sex. Currently it is male only.
######To fix this:
######input the weighting schemes for males in index 1 of list, females as index 2 of [dicionary]:[list] structure..

    

def age_scorer(Patients):
    #############################
    #Compute the age breakdown
    ################################
    varname="Age"
    agecuts=[0,34,39,44,49,54,59,64,69,74,110]
    
    #
    #something like weight_selector(age,sex,treatment,varname)
    
    agescores=[-9,-4,0,3,6,8,10,11,12,13]
    
    temp=pd.Series(pd.cut(Patients['Age'],bins=agecuts, labels=agescores))
    return temp


def cholest_scorer(Patients):
    ###########################
    ###select the apprpriate scores based on age and cholesterol
    ###########################
    
    cholest_criteria=[
                  [pat['Cholest']<160,
                  (pat['Cholest']>=160) & (pat['Cholest']<=199),
                  (pat['Cholest']>=200) & (pat['Cholest']<=239),
                  (pat['Cholest']>=240) & (pat['Cholest']<=279),
                  pat['Cholest']>=280]
                      for _, pat in Patients.iterrows()]
    
    
    cholest_scr=[]
    for index,pat in Patients.iterrows():
        
        age=pat['Age']
    
        if 30<=age<=39:
            TotalCol=[0,4,7,9,11]
            
        elif 40<=age<=49:
            TotalCol=[0,3,5,6,8]
            
        elif 50<=age<=59:
            TotalCol=[0,2,3,4,5]
            
        elif 60<=age<=69:
            TotalCol=[0,1,1,2,3]
            
        elif 70<=age<=79:
            TotalCol=[0,0,0,1,1]
        else:
            print("this person is over the validated age range")
            cholest_scr.append(np.nan)
        Patients_Chol=np.select(cholest_criteria[index], TotalCol ,np.nan)
        cholest_scr.append(Patients_Chol)
        
    temp=pd.Series(cholest_scr,name="Cholest_scr").astype(int)
    Patients=pd.concat([Patients, temp], axis=1)
    return Patients['Cholest_scr']
        
def smoke_scorer(Patients):
    ###########################
    ###select the apprpriate scores based on age and cholesterol
    ###########################
    smoke_scr=[]
    
    #establish criteria
    smoke_criteria=[[pat['Smoke']=="No",
                      pat['Smoke']=="Yes"]
                    for _, pat in Patients.iterrows()]
        
    
    for index,pat in Patients.iterrows():
    
        age=pat['Age']
    
        if 30<=age<=39:
            SmokeWgt=[0,8]
            
        elif 40<=age<=49:
            SmokeWgt=[0,5]
            
        elif 50<=age<=59:
            SmokeWgt=[0,3]
            
        elif 60<=age<=69:
            SmokeWgt=[0,1]
            
        elif 70<=age<=79:
            SmokeWgt=[0,1]
        else:
            print("this person is over the validated age range")
            smoke_scr.append(np.nan)
        Patients_smoke=np.select(smoke_criteria[index], SmokeWgt ,np.nan)
        smoke_scr.append(Patients_smoke)
        
    finalscores=pd.Series(smoke_scr,name="Smoke_scr").astype(int)
    return finalscores

    
def hdl_scorer(Patients):
#######Compute HDL Scoring###############
#####
######################################

    #REMEMBER- highest cut values = the TOP of the cut of, 0-*39*, 40-*49* unless right=True specified, 
    #then it reverses.
    
    cuts=[0, 39,49,59,150]
    
    HDLWgt=[-1,0,1,2]
    
    temp=pd.Series(pd.cut(Patients['HDL'], bins=cuts, labels=HDLWgt).astype(int))
    
    return temp
    
def systolic_scorer(Patients):
    #########################
    #########Systolic Scoring
    #########################
    
    #establish criteria

    systol_criteria=[[pat['Systolic']<120,
                    (pat['Systolic']>=120) & (pat['Systolic']<129),
                    (pat['Systolic']>=130) & (pat['Systolic']<139),
                    (pat['Systolic']>=140) & (pat['Systolic']<159),
                    pat['Systolic']>=160]
                     for _, pat in Patients.iterrows()]
    
    #establish empty list for storing approriate scores

    systol_scr=[]
        
    
    for index,pat in Patients.iterrows():
        
        treat=pat['Treat']
        if treat=="Yes":
            SystolicWgt=[0,1,2,2,3]
            
        elif treat=="No":
            SystolicWgt=[0,0,1,1,2]
        elif pat['Systolic']<30:
            print("this person is possibly dying,dead, or in serious trouble! \\\
                  Uh oh! Stop filling out the form and help them!")
            #they are invalid, so add missing and move on.
            systol_scr.append(np.nan)
    
        #use selection criteria to assign the appropriate score for that row. 
        Patients_Systolic=np.select(systol_criteria[index], SystolicWgt ,np.nan)
        systol_scr.append(Patients_Systolic)
    #bring it in to the appropriate DF. 
    temp=pd.Series(systol_scr,name="Systolic_scr").astype(int)
    return temp





#######################TESTING

import Scorers as scorer
import pandas as pd
import numpy as np
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
