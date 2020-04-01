# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 01:57:39 2020

@author: agarcia20
"""

import yfinance as yf                       
import math
 
stock = yf.Ticker("XOM")                                                                 # Get ticker
expiration = stock.options[0]                                                            # Get next expiration date
opt = stock.option_chain(expiration)                                                     # Get the option chain

options = opt.calls                                                                      # Get options
for idx_left_body, left_body in options.iterrows():                                      # Iterate over all options
    left_wings = options[options['strike'] < left_body['strike']]                        # Get left wings

    for idx_left, left in left_wings.iterrows():                                         # Iterate over left wings
        right_bodies = options[options['strike'] > left_body['strike']]                  # Get right bodies

        for idx_right_body, right_body in right_bodies.iterrows():                       # Iterate over right bodies
            right_wings = options[options['strike'] > right_body['strike']]              # Get right wings

            for idx_right, right in right_wings.iterrows():                              # Iterate over right wings
        
                left_count = round(right['strike'] - right_body['strike'], 2) * 1000     # Left raw wing/body count             
                right_count = round(left_body['strike'] - left['strike'], 2) * 1000      # Right raw wing/body count
    
                if (left_count == int(left_count) and right_count == int(right_count)):  # If there is a integer number of contracts try to minimize the quantity
                    gcd = math.gcd(int(left_count), int(right_count))                    # Greated Common Divisor between the number of contracts
        
                    left_count /= gcd
                    right_count /= gcd
                    
                    if left_count <= 10 and right_count <= 10:                           # Filter all the condors with less than 10 contracts
                        print("Buy %d Contract (Strike %.2f) - Sell %d Contract (Strike %.2f) - Sell %d Contract (Strike %.2f) - Buy %d Contract (Strike %.2f)" % 
                            (left_count, left['strike'], left_count, left_body['strike'], right_count, right_body['strike'], right_count, right['strike']))