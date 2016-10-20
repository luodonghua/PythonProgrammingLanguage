unique_name={'CAT','AA','IBM','GE','MSFT'}
namestr = ','.join(unique_name)
print(namestr) # GE,IBM,MSFT,CAT,AA

import urllib.request
u = urllib.request.urlopen('http://finance.yahoo.com/d/quotes.csv?s={}&f=l1'.format(namestr))
data = u.read()
print(data) # b'29.09\n152.075\n57.125\n86.855\n26.92\n'

pricedata = data.split()
print(pricedata) # [b'29.09', b'152.075', b'57.125', b'86.855', b'26.92']

for name, price in zip(unique_name, pricedata):
    print(name, '=', price)
'''
CAT = b'86.90'
MSFT = b'57.17'
IBM = b'152.15'
AA = b'26.94'
GE = b'29.10'
'''

prices = dict(zip(unique_name, pricedata))
print(prices) # {'MSFT': b'57.175', 'GE': b'29.09', 'IBM': b'152.1993', 'AA': b'26.94', 'CAT': b'86.9501'}

print (prices['IBM']) # b'152.19'

prices = {name: float(price) for name, price in zip(unique_name, pricedata)}
print (prices) # {'GE': 29.07, 'AA': 26.94, 'IBM': 152.37, 'MSFT': 57.235, 'CAT': 86.88}

print (prices['IBM']) # b'152.37'

