# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:37:43 2020

@author: sayers
"""
import math
import os
import pandas as pd
from datetime import datetime 
from matplotlib import pyplot as plt
import ast

def openstrip(filename):
    try:
        osdf = pd.read_excel(filename)
    except:
        print(f'{filename} failed during openstrip')
    osdf.columns = osdf.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    return(osdf)

def main(directory_in_str):
    pafdf = pd.DataFrame().astype('object')                #makes it so things can be stored in df that are lists
    directory = os.fsencode(directory_in_str)           #defines directory as indicated string
    os.chdir(directory)                                 #navigate to directory specified
    for file in os.listdir(directory):                  #iterates over all the files here
        filename = os.fsdecode(file)                    #specifies filename from file
        if filename.startswith("carep2020"):                  #isolates epub for further action
            try:
                x1212=openstrip(filename)
                pafdf = pafdf.append(x1212,ignore_index=True)  #appends results of function to df
            except:
                print(filename," failed during appending.")        #or lets you know it couldn't
        else:
            continue
    else:
        pafdf.to_excel('summaryoutput.xls',index=False)      #writes dataframe to csv file to save memory
    return(pafdf)
directory_in_str = 'S:\\Downloads\\'

df = pd.read_excel('S:\\Downloads\\alrep4292020.xls')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
df.columns = ['department', 'name', 'start', 'end', 'category', 'status', 'rate',
       'hours_appointed', 'hrs_used', 'ot_hrs', 'sft_hrs', 'hrs_bal',
       'earned_al', 'transf_al', 'used_al', 'balance_al', 'prior_sick',
       'earned_sick', 'transf_sick', 'used_sick', 'balance_sick']
df = df[df.category.isin(['C/A','CAP','ECA'])]
dfe=pd.read_excel('S:\\Downloads\\emplidrep.xlsx')
dfy=pd.read_excel('S:\\Downloads\\yoscur.xlsx')
dfe.columns = dfe.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
dfy.columns = dfy.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
dfy.columns = ['emplid','yrs']
df = (df.merge(dfe,how='left'))
df = df[df.department.isnull()==False]
df =df[df.emplid.isnull()==False]
df= df.astype({'emplid':'int64'})
dfy = dfy.groupby(['emplid'], sort=False)['yrs'].max()
df = df.merge(dfy, how="outer",left_on="emplid", right_on="emplid")
df = df[df.status.isin(['ACTIVE','INACT'])]
hrsdf = df.groupby(['emplid','department'])['hours_appointed'].sum()
cahrsdf = df.groupby(['emplid','department'])['hrs_used'].sum()

hrsdf.to_excel('s:\\downloads\\thisdumbshit.xls')
df = df[df.status=="ACTIVE"]

namelist = list(df.name.unique())
emplist = list(df.emplid.unique())
'''
#namelist=['HUGGINS, SHYANNE']
counter = 0.0
for i in namelist:
    total_hours = df[df.name==i].hours_appointed.sum()
    hrs_used = df[df.name==i].hrs_used.sum()
    al_earned = df[df.name==i].earned_al.sum()
    total_used_al = df[df.name==i].used_al.sum()
    al_bal = df[df.name==i].balance_al.sum()
    yrs = df[df.name==i].yrs.max()
    x = df[df.name==i].rate.max()
    if x<15.61:
        x=15.61
    al_rate = hrs_used/al_earned
    if math.isnan(al_rate):
        al_rate = 15
    aldue= (total_hours/al_rate)*x
    if al_bal<0.1 and total_hours<500: #if the current al is 0, they're new
        aldue=0
    if yrs>=3:
        aldue= (total_hours/al_rate)*x
    if 'ACTIVE' not in list(df[df.name==i].status.unique()):
        aldue=0
    counter+=aldue
    print(f'{i} will be due ${aldue} if they work {total_hours} hours and earn at a rate of {al_rate}')
else:
    print(f'total annual leave payout is estimated at {counter}')
'''    
counter = 0.0
dfx=pd.DataFrame(columns=(['empl','total_hours','hrs_used','al_earned','al_used','al_bal','yrs','accrual_rate','pay rate','projected_al','proj_al_amt']))
for i in emplist:
    #y=pd.DataFrame().astype('object')    
    total_hours = df[df.emplid==i].hours_appointed.sum()
    hrs_used = df[df.emplid==i].hrs_used.sum()
    al_earned = df[df.emplid==i].earned_al.sum()
    total_used_al = df[df.emplid==i].used_al.sum()
    al_bal = df[df.emplid==i].balance_al.sum()
    yrs = df[df.emplid==i].yrs.max()
    x = df[df.emplid==i].rate.max()
    if x<15.61:
        x=15.61
    try:
        al_rate = hrs_used/al_earned
        al_rate = round(al_rate,0)
    except:
        print(f"there's been an error with {i}. Al_rate is {al_rate}")
    if math.isnan(al_rate):
        al_rate = 15
    alhours = (total_hours/al_rate)
    aldue= (total_hours/al_rate)*x
    if al_bal<0.1 and total_hours<500: #if the current al is 0, they're new
        aldue=0
    if yrs>=3:
        aldue= (total_hours/al_rate)*x
    if 'ACTIVE' not in list(df[df.emplid==i].status.unique()):
        aldue=0
    counter+=aldue
    '''
    y[y.shape[1]]= i 
    y[y.shape[1]]= total_hours
    y[y.shape[1]]= hrs_used
    y[y.shape[1]]= al_earned
    y[y.shape[1]]= total_used_al
    y[y.shape[1]]= al_bal
    y[y.shape[1]]= yrs
    y[y.shape[1]]= al_rate
    y[y.shape[1]]= alhours
    y[y.shape[1]]= aldue'''
    to_append=[i,total_hours,hrs_used,al_earned,total_used_al,al_bal,yrs,al_rate,x,alhours,aldue]
    a_series = pd. Series(to_append, index = dfx.columns)
    dfx = dfx.append(a_series, ignore_index=True)
    #dfx = dfx.append([i,total_hours,hrs_used,al_earned,total_used_al,al_bal,yrs,al_rate,alhours,aldue])
    #print(f'{i} will be due ${aldue} if they work {total_hours} hours and earn at a rate of {al_rate}')
else:
    print(f'total annual leave payout is estimated at {counter}')
dfx.to_excel("s:\\downloads\\AnnualLeaveReport.xls")
dfx[(dfx.yrs>5)&(dfx.accrual_rate!=11)][['empl','yrs']]

dfx= pd.read_excel("s:\\downloads\\AnnualLeaveReport.xls")
dfx.columns = dfx.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
dfz = dfx[dfx['unnamed:_7']==0]
df['department','name','category','emplid' ]
dfa = dfz.merge(df[['department','name','category','emplid' ]], how="left",left_on="empl",right_on="emplid")
dfa = dfa.drop_duplicates()
dfa.to_excel("s:\\downloads\\CAusagereport.xls")

for i in dfx.empl.unique():
    if df[df.emplid==i].shape[0] >1:
        if dfx[dfx.empl==i].total_hours.values >1000:
            print(f'{i} - {dfx[dfx.empl==i].total_hours.values}')
            
def fordummies(df0,df1):
    return(carep2020df[(carep2020df['ss_#']==df0) & (carep2020df['dept']==df1)].bgn_date.min())

carep2020df = pd.read_excel('s:\\downloads\summaryoutput.xls')
carep2020df.bgn_date=pd.to_datetime(carep2020df['bgn_date'])
carep2020df.groupby(['ss_#','dept'])['bgn_date'].min()
deptsrep = carep2020df[['dept','deptarment_name']]
deptsrep = deptsrep.drop_duplicates()
carep = carep2020df[['ss_#','dept']]
carep = carep.drop_duplicates()
carep.columns = ['empl','dept']
carep['dept_start']= carep.apply(lambda x: fordummies(x.empl, x.dept), axis=1)
carep = carep.merge(deptsrep,how='left')
from datetime import datetime as dt

def yosfunc(df0,df1):
    try:
        if ((dt.today() - df1)/365.2425) > dfy.loc[df0]:
            return(df1)
        else:
            return(datetime.datetime.now() - datetime.timedelta(yeasr=dfy.loc[df0]))
    except:
        print("no luck boss")
        return(df1)

carep['1']=carep.apply(lambda x: yosfunc(x.empl, x.dept_start), axis=1)
dfy.loc[10981641]
carep.to_excel('s:\\downloads\\shitdrivingmenuts.xls')