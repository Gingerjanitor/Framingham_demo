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
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.compat import lzip
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms


wb=load_workbook("C:/Users/Matt0/test project/Framingham score tool/Script.xlsx")
ws=wb.active

def gendata(Patients):
    np.random.seed(29293)
    Patients['tempcost']=np.random.randint(85,10000, 250)
    #Impose a correlation between this new variable and Framingham scores
    Patients['Annual_med_costs']=(Patients['Framingham']+.002*Patients['tempcost'])*100
    del Patients['tempcost']


    #An indicator of if they are a snap recipient or not
    Patients['SNAP']=np.random.default_rng().choice(["no","yes"],len(Patients['Gender']))
    #doctor it so Patients is correlated with high risk by randomly assigning some of the snap people to be high risk.
    rand=np.random.randint(0,100,250)
    Patients.loc[(rand>=35) & (Patients['Highrisk']==">20% risk"), 'SNAP']="yes"

    #dummy up gender and SNAP for later
    Patients['Male']=pd.get_dummies(Patients['Gender'],drop_first=True, dtype=float)
    Patients['SNAP_yes']=pd.get_dummies(Patients['SNAP'], drop_first=True, dtype=float)

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
            
        input("\n\n Press enter when you're finished")

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

    
        explain=str(input("\n Shall I provide an interpretation of these results and next steps? Enter Y or N?\n"))
        while explain.lower() not in ['y','n']:
            
            explain=str(input("Please enter either Y or N \n"))
    
        if explain.lower()=="y":
            print("\n\n_____________________________________________\n\n")
            print(ws['G3'].value)
            input("\n\n Press enter when you're finished")

def makehistogram(Patients):
        
    costanalysis=input(ws['I2'].value)
    while costanalysis.lower() not in ['y','n']:
        costanalysis=str(input("Please enter either Y or N \n"))
    
    if costanalysis.lower()=="y":
        print("\n\n_____________________________________________\n\n")  
        print("First, it is important to examine distributions for both variables.\n\n")
          
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        f, axes = plt.subplots(1, 2)
        
        sns.histplot(data=Patients,
                     x='Risk_pct',
                     bins=20,
                     ax=axes[0])
        axes[0].set_xlabel("10-year risk %")
        axes[0].set_title("Framingham Risk Estimate Distribution")
        axes[0].axvline(x=Patients['Risk_pct'].mean(),color='red')
        axes[0].axvline(x=Patients['Risk_pct'].median(),color='blue')
        
        sns.histplot(Patients['Annual_med_costs'],
                     bins=20,
                     ax=axes[1])
        axes[1].set_title("Annual Medical Costs Distribution")
        axes[1].set_xlabel("$ Spent Per Year")
        axes[1].axvline(x=Patients['Annual_med_costs'].mean(),color='red')
        axes[1].axvline(x=Patients['Annual_med_costs'].median(),color='blue')
        
        plt.show()
        
        explain=str(input("\n Would you like an explanation of these graphs? Enter Y or N?\n"))
        while explain.lower() not in ['y','n']:
            
            explain=str(input("Please enter either Y or N \n"))
    
        if explain.lower()=="y":
            print("\n\n_____________________________________________\n\n")
            explanation=ws['I3'].value
            mean=int(Patients['Annual_med_costs'].mean())
            std=int(Patients['Annual_med_costs'].std())
            stdrange=int(std*1.96)
            explanation=explanation.replace('PATIENTMEAN',f'${mean}')
            explanation=explanation.replace('PATIENTSTD',f'${std}')
            explanation=explanation.replace('STDRANGE',f'${stdrange}')
            input(explanation)
            
def runscatter(Patients):
    
###Scatter plots

###display the first
    input(ws['I4'].value)
    plt.figure(figsize=(8, 5))
    sns.regplot(x = "Risk_pct", y = "Annual_med_costs", data = Patients)
    plt.title("Correlation between Framingham scores \n and medical expenditures", fontsize=18)
    plt.xlabel("10-year risk %", fontsize=15)
    plt.ylabel("Annual medical expenditures", fontsize=15)
    plt.show()
    
    print("\n_____________________________________________\n")
    
    ##display the second
    input(ws['I5'].value)
    
    print("\n_____________________________________________\n")
    plt.figure(figsize=(8, 5))
    sns.lmplot(x = "Risk_pct", y = "Annual_med_costs",
               hue = "Gender", 
               markers = ["s", "x"],
               data = Patients,
               legend=False,
               facet_kws={'legend_out': True},
               height=5,
               aspect=1.5)
    plt.legend(title="Gender", loc="upper left", bbox_to_anchor=(.75, .25))
    plt.title("Highlighting sex differences", fontsize=18)
    plt.xlabel("10-year risk %", fontsize=15)
    plt.ylabel("Annual medical expenditures", fontsize=15)
    
    plt.show()
    interpretplz=input(ws['I6'].value)
    while interpretplz.lower() not in ['y','n']:
        interpretplz=str(input("Please enter either Y or N \n"))
    
    if interpretplz=="y":
        answer=ws['I7'].value
        answer=answer.replace("CORRCOEF",f"{Patients['Risk_pct'].corr(Patients['Annual_med_costs']).round(2)}")
        print("\n")
        input(answer)
        
        
        
def OLSdemo(Patients):
    ####Do a regression model and diagnostics
    
    # predictor = sm.add_constant(Patients['Risk_pct'])
    # model=sm.OLS(Patients['Annual_med_costs'],predictor).fit()
    # output=model.summary()
    # print(output)
    
    #more covs
    print("\n\n_____________________________________________\n\n")
    
    input(ws['I8'].value)
    
    model=smf.ols('Annual_med_costs~Risk_pct+Male+SNAP_yes',data=Patients)
    output=model.fit()
    print(output.summary())
    
    print("\n\n_____________________________________________\n\n")
    
    print("Above are the base model estimates.")
          
    
    options=input(ws['I9'].value)
    while options not in ['1','2','3','4']:
            options=input("You have to enter a value from 1 to 4")
    
           
    while options!='4':
        if options=='1':
        ##standardized coefs
            Patients['Annual_med_costs_Beta']=stats.zscore(Patients['Annual_med_costs'])
            
            Patients['Risk_pct_Beta']=stats.zscore(Patients['Risk_pct'])
            Patients['SNAP_yes_Beta']=stats.zscore(Patients['SNAP_yes'])
            Patients['Male_Beta']=stats.zscore(Patients['Male'])
            
            
            varliststd=Patients[['Risk_pct_Beta','SNAP_yes_Beta','Male_Beta']]
            varliststd = sm.add_constant(varliststd)
            varliststd_standardized = (varliststd - varliststd.mean()) / varliststd.std()
            
            # Fit the model
            modelstd = sm.OLS(Patients['Annual_med_costs_Beta'], varliststd).fit()
            outputstd=modelstd.summary()
            print(outputstd)
            
            input("\n\n*********Press enter to go back to the menu*********")
        
        if options=='2':
            print("\n\n_____________________________________________\n\n")
            input("We'll start with a residual vs fitted plots and other similar tools. Press enter to show.")
            diags = plt.figure(figsize=(12,8))
            sm.graphics.plot_regress_exog(output, 'Risk_pct', fig=diags)
            plt.show(diags)
            
            print("\n\n_____________________________________________\n\n")
    
            input("Press enter to show a graph of potential outliers using Cook's D. ")
            fig = sm.graphics.influence_plot(output, criterion="cooks")
            fig.tight_layout(pad=1.0)
            plt.show(fig)
            
            print("\n\n_____________________________________________\n\n")
    
            input("Press enter to see the distribution of residuals")
            resid=output.resid
            sns.histplot(resid)
            plt.title("Residual Error")
            plt.show(fig)
            print("\n\n_____________________________________________\n\n")
    
            input("\n\nPress enter to see results from the Breusch-Pagan Lagrangian multiplier test for heteroskedascticity ")
            name = ['Lagrange multiplier statistic', 'p-value', 'f-value', 'f p-value']
            test = sm.stats.het_breuschpagan(output.resid, output.model.exog)
            print(lzip(name, test))
            
            input("\n\n*********Press enter to go back to the menu*********")
        
        if options=='3':
            print("\n\n_____________________________________________\n\n")
            print(ws['I10'].value)
            input("\n\n*********Press enter to go back to the menu*********")
    
        print("\n\n_____________________________________________\n\n")
    
        options=input(ws['I9'].value)
        while options not in ['1','2','3','4']:
                options=input("You have to enter a value from 1 to 4")
    print("\n\n_____________________________________________\n\n")
    
    input("Moving on, in light of those diagnostics we should fit the model with a square term for risk scores. \n\n Press enter to do that.")
    
    model=smf.ols('Annual_med_costs~Risk_pct+I(Risk_pct**2)+Male+SNAP_yes',data=Patients)
    result=model.fit()
    print(result.summary())
    
    print("\n\n_____________________________________________\n\n")
    
    #say we need to graph it
    input(ws['I11'].value)
    
    
    model=smf.ols('Annual_med_costs~Risk_pct+I(Risk_pct**2)',data=Patients)
    result=model.fit()
    
    fig = sm.graphics.plot_fit(result,'Risk_pct', vlines=False)
    plt.show(fig)
    
    print("\n\n_____________________________________________\n\n")
    
    #Conclude the section.
    input(ws['I12'].value)
    
    
    
