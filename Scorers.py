# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:43:14 2023

@author: Matt0

#This file establishes the functions that are used to convert raw patient data to scored data
"""
import pandas as pd
import numpy as np
import Scorers as scorer
import Weight_selector as ws

#Scoring sheet can be found here https://onlinelibrary-wiley-com.ezproxy.clarkson.edu/doi/pdf/10.1002/sim.1742

######
######The scoring criteria are different based on sex. Currently it is male only.
######To fix this:
######input the weighting schemes for males in index 1 of list, females as index 2 of [dicionary]:[list] structure..

    

def age_scorer(Patients):
    #############################
    #Compute the age breakdown
    ################################
    
    agecuts=[0,34,39,44,49,54,59,64,69,74,110]
    agelist=[]
    #
    for index,pat in Patients.iterrows():
        age=pat['Age']

        wgtset=ws.weight_selector("Age",pat['Gender'],pat['Age'],pat['Treat'])

        score=pd.cut([age],bins=agecuts,labels=wgtset).astype(int)

        agelist.append(score[0])
    
    temp=pd.Series(agelist)
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
    
    cholestlist=[]
    for index,pat in Patients.iterrows():
        wgtset=ws.weight_selector("Cholest",pat['Gender'],pat['Age'],pat['Treat'])
        score=np.select(cholest_criteria[index],wgtset, np.nan).astype(int)
        cholestlist.append(score)
            
    temp=pd.Series(cholestlist).astype(int)
    return temp

        
def smoke_scorer(Patients):
    ###########################
    ###select the apprpriate scores based on age and cholesterol
    ###########################
    
    #establish criteria
    smoke_criteria=[[pat['Smoke']=="No",
                      pat['Smoke']=="Yes"]
                    for _, pat in Patients.iterrows()]
        
    
    for index,pat in Patients.iterrows():
    
        smokelist=[]
        for index,pat in Patients.iterrows():
            wgtset=ws.weight_selector("Smoke",pat['Gender'],pat['Age'],pat['Treat'])
            score=np.select(smoke_criteria[index],wgtset, np.nan).astype(int)
            smokelist.append(score)
                
        temp=pd.Series(smokelist).astype(int)
        return temp

    
def hdl_scorer(Patients):
#######Compute HDL Scoring###############
#####
######################################

    #REMEMBER- highest cut values = the TOP of the cut of, 0-*39*, 40-*49* unless right=True specified, 
    #then it reverses.
    
    cuts=[0, 39,49,59,150]
    
    #This one is fixed regardless of age and gender, so no weight selector fn.
    #notice that the order is reversed, since 
    HDLWgt=[2,1,0,-1]
    
    temp=pd.Series(pd.cut(Patients['HDL'], bins=cuts, labels=HDLWgt).astype(int))
    
    
    return temp
    
def systolic_scorer(Patients):
    #########################
    #########Systolic Scoring
    #########################
    
    #establish criteria

    systol_criteria=[[pat['Systolic']<120,
                    (pat['Systolic']>=120) & (pat['Systolic']<=129),
                    (pat['Systolic']>=130) & (pat['Systolic']<=139),
                    (pat['Systolic']>=140) & (pat['Systolic']<=159),
                    pat['Systolic']>=160]
                     for _, pat in Patients.iterrows()]
    
    #establish empty list for storing approriate scores

    systollist=[]
    for index,pat in Patients.iterrows():

        wgtset=ws.weight_selector("Systolic",pat['Gender'],pat['Age'],pat['Treat'])
        score=np.select(systol_criteria[index],wgtset, np.nan).astype(int)
        systollist.append(score)


    if pat['Systolic']<30:
            print(f"Patient {pat.index} is possibly dying,dead, or in serious trouble! \\\
                  Uh oh! Stop filling out the form and help them!")
            #they are invalid, so add missing and move on.
            systollist.append(np.nan)
            
    temp=pd.Series(systollist).astype(int)
    return temp


#######################TESTING
