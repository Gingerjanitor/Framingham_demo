# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:22:25 2023

@author: Matt0
"""

import pandas as pd
import numpy as np


def risk_assign(pat, sex):
    #remember that there are cutoffs for both that must be computed first
    #I code them to -1 so they get put to the right category
    #MEN
    #lt0=1
    #0-4=2
    #5-6=3
    #6-16 are uniquely risk correlated, keep them
    #17+=17
    
    #Women
    # <9=1
    # 9-12=2
    # 13-14=3
    # 25=25+
    
    tempdf=pd.concat([pat,sex],axis=1)
                     
    ###Recode for men...
    #There's probably a more efficient way, but it runs!
    tempdf.loc[(tempdf['Framingham']<0) & (tempdf['Gender']=="M"),'tempcollapse']=1
    tempdf.loc[(tempdf['Framingham']>=0) & (tempdf['Framingham']<=4 ) & (tempdf['Gender']=="M"),'tempcollapse']=2
    tempdf.loc[(tempdf['Framingham']>=5) & (tempdf['Framingham']<=6) & (tempdf['Gender']=="M"),'tempcollapse']=3
    tempdf.loc[(tempdf['Framingham']>=17) & (tempdf['Framingham']<=45) & (tempdf['Gender']=="M"),'tempcollapse']=17
            #this one replaces missings with values.
    tempdf.loc[(tempdf['tempcollapse'].isna()==True) & (tempdf['Gender']=="M"),'tempcollapse']=tempdf['Framingham']
    
    #recode for women [there's GOT to be a better way for this that I'm blanking]
    tempdf.loc[(tempdf['Framingham']<9) & (tempdf['Gender']=="F"),'tempcollapse']=1
    tempdf.loc[(tempdf['Framingham']>=9) & (tempdf['Framingham']<=12 ) & (tempdf['Gender']=="F"),'tempcollapse']=2
    tempdf.loc[(tempdf['Framingham']>=13) & (tempdf['Framingham']<=14) & (tempdf['Gender']=="F"),'tempcollapse']=3
    tempdf.loc[(tempdf['Framingham']>=25) & (tempdf['Framingham']<=45) & (tempdf['Gender']=="F"),'tempcollapse']=25
            #this one replaces missings with values.
    tempdf.loc[(tempdf['tempcollapse'].isna()==True) & (tempdf['Gender']=="F"),'tempcollapse']=tempdf['Framingham']
    
    
    ############
    ##Establish their risk level according to study
    ############
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
    
    risklist=[]
    for temp in tempdf.itertuples():
        risk_level=risk_tables[temp.Gender][temp.tempcollapse]
        risklist.append(risk_level)
    
    risk=pd.Series(risklist,name="Risk_pct")
    tempdf=pd.concat([tempdf,risk],axis=1)
    
    ######Create two risk indicators
    ######One categorical 0-4, 5-9,10-14,15-20,20+
    
    riskcatcut=[-1,5,10,15,20,50]
    riskcatlabels=["0-4% risk","5-9% risk", "10-14% risk", "15-19% risk", "20+% risk"]
    riskcatraw=[0,1,2,3,4]
    tempdf['Riskcatsnum']=pd.cut(tempdf['Risk_pct'],bins=riskcatcut,labels=riskcatraw,right=False)
    tempdf['Riskcats']=pd.cut(tempdf['Risk_pct'],bins=riskcatcut,labels=riskcatlabels,right=False)
    
    
    ######A second that is just high risk people. That is, you're a core above or below 20
    
    highriskcut=[-1,20,50]
    highrisklabel=["<20% risk",">20% risk"]
    highriskraw=[0,1]
    tempdf['Highrisknum']=pd.cut(tempdf['Risk_pct'],bins=highriskcut,labels=highriskraw)

    tempdf['Highrisk']=pd.cut(tempdf['Risk_pct'],bins=highriskcut,labels=highrisklabel)
    
    tempdf=tempdf.drop(['Framingham','Gender','tempcollapse'],axis=1)
    
    return tempdf