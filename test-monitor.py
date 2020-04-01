import pandas as pd
import pyfolio as pf
import yfinance as yf

"""
Bajamos la info de Yahoo Finance
"""
cartera = ['GGAL.BA','GGAL']

data = yf .download('GGAL.BA GGAL', period='2d')

print(data)
"""
Buscamos los datos de cierre ant USA y Apertura Byma
para evaluar potenciales arbitrajes
"""
adrclose = data['Adj Close']['GGAL'].iloc[0]
locopen = data['Open']['GGAL.BA'].iloc[1]
factor=10
ccl = 81.85

arbitrado = ( adrclose/factor ) * (ccl)

"""
Utilizamos series para calcular la diff
entre el local y el arbitrado con pct_change
"""
s = pd.Series([arbitrado,locopen])
diff=s.pct_change().iloc[1]

"""
Armamos la tabla final de arbitrajes
TODO: Agregar el resto de ADRS
"""

dict = {"Name": ["GGAL"],
       "Conversion": [factor],
       "ADR": [adrclose],
       "Arbitrado": [arbitrado], 
       "Local": [locopen],
       "Diff":[diff]}

result = pd.DataFrame(dict)
print(result)
