# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 02:17:24 2020

@author: agarcia20
"""

#import bjerksund_stensland as md
import bolsuite as bs
import pandas as pd
import mibian

bsc = bs.Connector()

df_data = bsc.bluechips(ticker='GGAL', settlement='48hs')
underlying_price = df_data.loc['GGAL','Close'].item()
#print(df_data.columns.values)
#print(df_data)

df_opt = bsc.options(underlying_asset='GGAL') 
#print(df_opt.columns.values)
#print(df_opt)
#print(df_opt.query('Symbol == "GFGC102.AB"'))

# iterate through each row and select  
# and complete columns with Greeks and Volatility
vi = []
vega=[]
gamma=[]
delta=[]
theta=[]
for index, row in df_opt.iterrows(): 
    if (row["Kind"] == 'Call'):
        c = mibian.BS([underlying_price, row["Strike"], 2, (row["Expiration"] - pd.Timestamp.today()).days], callPrice=row["Close"])
        vi.append( c.impliedVolatility)
        c = mibian.BS([underlying_price, row["Strike"], 2, (row["Expiration"] - pd.Timestamp.today()).days], volatility=c.impliedVolatility)
        delta.append(c.callDelta)
        theta.append(c.callTheta)
    if (row["Kind"] == 'Put'):
        c = mibian.BS([underlying_price, row["Strike"], 2, (row["Expiration"] - pd.Timestamp.today()).days], putPrice=row["Close"])
        vi.append( c.impliedVolatility)
        c = mibian.BS([underlying_price, row["Strike"], 2, (row["Expiration"] - pd.Timestamp.today()).days], volatility=c.impliedVolatility)
        delta.append(c.putDelta)
        theta.append(c.putTheta)
    gamma.append(c.gamma)
    vega.append(c.vega)    
 #   vi.append( c.impliedVolatility)

df_opt["VI"] = vi
df_opt["Delta"] = delta
df_opt["Gamma"] = gamma
df_opt["Theta"] = theta
df_opt["Vega"] = vega
    #print((row["Expiration"] - pd.Timestamp.today()).days)
    #print (type(row["Expiration"]) )

print(df_opt)
df_opt.to_csv(r'GGALoptions.csv', index = False)
#GFGC102.AB


#underlying_price = df_data.loc['GGAL','Close'].item()
#exercise_price = df_opt.loc['GFGC75.0AB','Strike'].item()
#time_in_years = 24/365
#risk_free_rate = 0.02
#option_price = df_opt.loc['GFGC75.0AB','Close'].item()
#print(underlying_price)

#print(exercise_price)
#print(option_price)

# Call Implied Volatility
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   option_price: It is the market price of the option
#iv =  md.implied_volatility_call(underlying_price, exercise_price, time_in_years, risk_free_rate, option_price)
#print(iv)
