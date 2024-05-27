#import required libraries
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# URL and parameters
'''remove # from token in below line''' 
# token = 256265
timeframe = "week"

# Start date
sdt = datetime(year=2019, month=2, day=2)

# End date (current date)
edt = datetime.now()

# Replace with your actual enctoken
enctoken = ""

header = {
    "Authorization": f"enctoken {enctoken}"
}

url = f"https://kite.zerodha.com/oms/instruments/historical/{token}/{timeframe}"
param = {
    "oi": 1,
    "from": sdt.strftime('%Y-%m-%d'),
    "to": edt.strftime('%Y-%m-%d')
}

session = requests.session()
response = session.get(url, params=param, headers=header)
data = response.json()["data"]["candles"]

df = pd.DataFrame(data)
print(df)
