# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 02:15:13 2020

@author: agarcia20
"""

from math import * 

# Cumulative standard normal distribution
def cdf(x):
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

# Intermediate calculation used by both the Bjerksund Stensland 1993 and 2002 approximations
def phi(s, t, gamma, h, i, r, a, v):
    lambda1 = (-r + gamma * a + 0.5 * gamma * (gamma - 1) * v**2) * t
    dd = -(log(s / h) + (a + (gamma - 0.5) * v**2) * t) / (v * sqrt(t))
    k = 2 * a / (v**2) + (2 * gamma - 1)

    try:
        return exp(lambda1) * s**gamma * (cdf(dd) - (i / s)**k * cdf(dd - 2 * log(i / s) / (v * sqrt(t))))
    except OverflowError as err:
        return exp(lambda1) * s**gamma * cdf(dd)

# Call Price based on Bjerksund/Stensland Model
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   volatility: Volatility percentage (ie. 30% volatility is 0.30)
def bjerksund_stensland_call(underlying_price, exercise_price, time_in_years, risk_free_rate, volatility):
    div = 1e-08
    z = 1
    rr = risk_free_rate
    dd2 = div
    
    dt = volatility * sqrt(time_in_years)
    drift = risk_free_rate - div
    v2 = volatility**2
    
    b1 = sqrt((z * drift / v2 - 0.5)**2 + 2 * rr / v2)
    beta = (1 / 2 - z * drift / v2) + b1
    binfinity = beta / (beta - 1) * exercise_price
    bb = max(exercise_price, rr / dd2 * exercise_price)
    ht = -(z * drift * time_in_years + 2 * dt) * bb / (binfinity - bb)
    i = bb + (binfinity - bb) * (1 - exp(ht))

    if underlying_price < i and beta < 100:
        alpha = (i - exercise_price) * i**(-beta)
        return alpha * underlying_price**beta - alpha * phi(underlying_price, time_in_years, beta, i, i, rr, z * drift, volatility) + phi(underlying_price, time_in_years, 1, i, i, rr, z * drift, volatility) - phi(underlying_price, time_in_years, 1, exercise_price, i, rr, z * drift, volatility) - exercise_price * phi(underlying_price, time_in_years, 0, i, i, rr, z * drift, volatility) + exercise_price * phi(underlying_price, time_in_years, 0, exercise_price, i, rr, z * drift, volatility)
    
    return underlying_price - exercise_price

# Put Price based on Bjerksund/Stensland Model
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   volatility: Volatility percentage (ie. 30% volatility is 0.30)
def bjerksund_stensland_put(underlying_price, exercise_price, time_in_years, risk_free_rate, volatility):
    div = 1E-08
    z = -1
    rr = div
    dd = rr
    dd2 = 2 * dd - rr
    asset_new = underlying_price
    underlying_price = exercise_price
    exercise_price = asset_new

    dt = volatility * sqrt(time_in_years)
    drift = risk_free_rate - div
    v2 = volatility**2

    b1 = sqrt((z * drift / v2 - 0.5)**2 + 2 * rr / v2)
    beta = (1 / 2 - z * drift / v2) + b1
    binfinity = beta / (beta - 1) * exercise_price
    bb = max(exercise_price, rr / dd2 * exercise_price)
    ht = -(z * drift * time_in_years + 2 * dt) * bb / (binfinity - bb)
    i = bb + (binfinity - bb) * (1 - exp(ht))
        
    if underlying_price < i and beta < 100: # To avoid overflow
        alpha = (i - exercise_price) * i**(-beta)
        return alpha * underlying_price**beta - alpha * phi(underlying_price, time_in_years, beta, i, i, rr, z * drift, volatility) + phi(underlying_price, time_in_years, 1, i, i, rr, z * drift, volatility) - phi(underlying_price, time_in_years, 1, exercise_price, i, rr, z * drift, volatility) - exercise_price * phi(underlying_price, time_in_years, 0, i, i, rr, z * drift, volatility) + exercise_price * phi(underlying_price, time_in_years, 0, exercise_price, i, rr, z * drift, volatility)
    
    return underlying_price - exercise_price    

# Call Implied Volatility
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   option_price: It is the market price of the option
def implied_volatility_call(underlying_price, exercise_price, time_in_years, risk_free_rate, option_price):
    high = 5
    low = 0

    while (high - low) > 0.0001:
        if bjerksund_stensland_call(underlying_price, exercise_price, time_in_years, risk_free_rate, (high + low) / 2) > option_price:
            high = (high + low) / 2
        else:
            low = (high + low) / 2
    
    return (high + low) / 2

# Put Implied Volatility
# Parameters
#   underlying_price: Price of underlying asset
#   exercise_price: Exercise price of the option
#   time_in_years: Time to expiration in years (ie. 33 days to expiration is 33/365)
#   risk_free_rate: Risk free rate (ie. 2% is 0.02)
#   option_price: It is the market price of the option
def implied_volatility_put(underlying_price, exercise_price, time_in_years, risk_free_rate, option_price):
    high = 5
    low = 0
    
    while (high - low) > 0.0001:
        if bjerksund_stensland_put(underlying_price, exercise_price, time_in_years, risk_free_rate, (high + low) / 2) > option_price:
            high = (high + low) / 2
        else:
            low = (high + low) / 2
    
    return (high + low) / 2