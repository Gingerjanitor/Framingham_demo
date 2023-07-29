# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:22:25 2023

@author: Matt0
"""
import pandas as pd
import numpy as np

#def risk_assign(pat, sex):
    
Patients=pd.read_csv(r"C:\Users\Matt0\test project\Framingham score tool\Patients temp.csv")

framingham= Patients['Framingham']
gender= Patients['Gender']
#remember that there are cutoffs for both that must be computed first
#I code them to -1 so they get put to the right category
#MEN
#lt0=1
#0-4=2
#5-6=3
#6-16 are uniquely risk correlated, keep them
#17+=17
tempdf=pd.concat([framingham,gender],axis=1)

for index,rows in tempdf.iterrows():
    if rows['Gender']=="M":
        print("test")
        tempdf.loc[tempdf['Framingham']<0,'tempcollapse']=1
        tempdf.loc[(tempdf['Framingham']>=0) & (tempdf['Framingham']<=4),'tempcollapse']=2
        tempdf.loc[(tempdf['Framingham']>=5) & (tempdf['Framingham']<=6),'tempcollapse']=3

        tempdf.loc[(tempdf['Framingham']>=17) & (tempdf['Framingham']<=45),'tempcollapse']=17
        #this one replaces missings with values.
        tempdf.loc[tempdf['tempcollapse'].isna()==True,'tempcollapse']=tempdf['Framingham']

    if tempdf['Gender'][index]=="F":
        print("poop")
    
    


risk_temp=pd.Series(collapse,name="collapse")
risk_temp=framingham.loc[framingham<=0]=10005050




for index,value in framingham.items():
    if gender[index]=="M":
        risk_temp[index]=ue<=0]=100000
    
    
    
temp=pd.concat([risk_temp,framingham], axis=1)
                    df_store.loc[df_store['Age']<30,"age_group"]="Young"

elif gender=="F"


#Women: 
#lt 9=0
#

risk_tables={'M':
                 {1:0,
                  2:1,
                  3:2,
                  7:3,
                  8:4,
                  9:5,
                  10:6,
                  11:8,
                  12:10,
                  13:12,
                  14:16,
                  15:20,
                  16:25,
                  17:30},
            'F':{1:0,
                  2:1,
                  3:2,
                  15:3,
                  16:4,
                  17:5,
                  18:6,
                  19:8,
                  20:11,
                  21:14,
                  22:17,
                  23:22,
                  24:27,
                  25:30}}