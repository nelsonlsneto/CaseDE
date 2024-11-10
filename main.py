# 1) IMPORTS
import pyspark
import requests
import json
import math
import pandas as pd

# 2) REQUEST

# 2.1) Finding out the number of breweries
url = 'https://api.openbrewerydb.org/v1/breweries/meta'

response = requests.request("GET", url = url)

num_brew = int(response.json()['total'])

# 2.2) 

num_req = math.ceil((num_brew/200))

list_brew = []

for i in range(0, num_req + 1):
    url = f'https://api.openbrewerydb.org/v1/breweries?page={i}&per_page=200'

    response = requests.request("GET", url = url)

    list_brew.extend(response.json())

pd.DataFrame(list_brew)