# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:29:14 2020

@author: agarcia20
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn

def call_payoff(sT, strike_price, premium):
    return (np.where(sT > strike_price, sT - strike_price, 0) - premium)*100

########### Market Data (Example)

# Stock price 
spot_price = 100

# Long call
strike_price_long_call = 140 
premium_long_call = 1.0

# Short call
strike_price_short_call = 130 
premium_short_call = 1.7

# Stock price range at expiration of the call 
sT = np.arange(50,150,1)

###########    
# Bear Call Spread
###########
payoff_long_call = call_payoff(sT, strike_price_long_call, premium_long_call)
payoff_short_call = call_payoff(sT, strike_price_short_call, premium_short_call) * -1.0

payoff = payoff_long_call + payoff_short_call

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT,payoff,label='%s/%s Call Spread' %(strike_price_short_call,strike_price_long_call),color='g')
plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.legend()

plt.grid( ls = '-.', lw = 0.25)


#Calculate P/L
profit = max (payoff)
loss = min (payoff)
margin = ((strike_price_long_call - strike_price_short_call)*100 - profit )
ret = (profit / margin)*100

ax.text(.1, .25, "Max Profit: %.2f\nMax Loss %.2f\nMargin %.2f\nReturn %.2f%%" %(profit, loss,margin,ret),
        bbox={'facecolor': 'yellow', 'alpha': 0.5, 'pad': 10},
        horizontalalignment='left',
        verticalalignment='bottom', 
        transform=ax.transAxes        
        )

plt.show()
