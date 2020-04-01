# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:16:50 2020

@author: agarcia20
"""

import pyRofex
import json

# Set the the parameter for the REMARKET environment
pyRofex.initialize(user="genangus3328",
                   password="vtmccT9#",
                   account="REM3328",
                   environment=pyRofex.Environment.REMARKET)

# Gets all segments
#p = pyRofex.get_segments()
#print(json.dumps(p, indent=1))
# Gets available instruments list
#p = pyRofex.get_all_instruments()
#print(json.dumps(p, indent=1))

# Gets detailed instruments list
#p = pyRofex.get_detailed_instruments()
#print(json.dumps(p, indent=1))

# Makes a request to the Rest API and get the last price
# Use the MarketDataEntry enum to specify the data
p = pyRofex.get_market_data(ticker="I.RFX20",
                        entries=[pyRofex.MarketDataEntry.LAST])
#p = pyRofex.get_market_data(ticker="I.RFX20")

print(json.dumps(p, indent=1))