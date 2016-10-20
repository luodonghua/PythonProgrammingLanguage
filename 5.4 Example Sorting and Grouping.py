import datetime
import csv

def read_csv(filename, errors='warn'):
    '''
    Read the CSV into a list
    '''

    if errors not in {'warn', 'silent', 'raise'}:
        raise ValueError("errors must be in one of 'warn', 'silent', 'raise'")

    airports = []       # list of records
    total = 0.0
    with open(filename,'r') as f:
            rows = csv.reader(f)
            headers = next(rows)           # Skill a single line input
            rowno = 0
            for rowno, row in enumerate(rows, start=1):
                try:
                    row[5] = float(row[5])
                    row[6] = float(row[6])
                    row[7] = datetime.datetime.strptime(row[7], '%Y-%m-%d')
                except ValueError as err: # Exception is the top level exception to catch all (dangerous)
                    if errors == 'warn':
                        print('Row:', rowno, 'Bad row:', row)
                        print('Row:', rowno, 'Reason:', err)
                    elif errors == 'raise':
                        raise      # Re-raise the last exception
                    else:
                        pass
                    continue    # skip to the next line
                record = {
                    'iata':row[0],
                    'title':row[1],
                    'city':row[2],
                    'state':row[3],
                    'country':row[4],
                    'latitude':row[5],
                    'longitude':row[6],
                    'opendate':row[7]
                }
                airports.append(record)
    return airports

def get_opendate(airport):
    return airport['opendate']

airports = read_csv('airports.csv', errors='silent')

airports.sort(key=get_opendate)

for i in range(3):
    print(airports[i]['title'],airports[i]['opendate'])
    '''
    Thigpen 1993-04-28 00:00:00
    Memphis Memorial 1995-03-21 00:00:00
    Columbiana County 2001-03-15 00:00:00
    '''

# lambda operation remove the steps of function definition
airports.sort(key=lambda airport: airport['opendate'])

for i in range(3):
    print(airports[i]['title'],airports[i]['opendate'])
    '''
    Thigpen 1993-04-28 00:00:00
    Memphis Memorial 1995-03-21 00:00:00
    Columbiana County 2001-03-15 00:00:00
    '''

print(min(airports, key=lambda airport: airport['opendate']))
# {'longitude': -89.23450472, 'title': 'Thigpen', 'country': 'USA', 'opendate': datetime.datetime(1993, 4, 28, 0, 0), 'iata': '00M', 'state': 'MS', 'city': 'Bay Springs', 'latitude': 31.95376472}

print(max(airports, key=lambda airport: airport['title']))
#{'longitude': -88.20111111, 'title': 'Tishomingo County', 'country': 'USA', 'opendate': datetime.datetime(2013, 5, 21, 0, 0), 'iata': '01M', 'state': 'MS', 'city': 'Belmont', 'latitude': 34.49166667}


import itertools
for opendate, airport in itertools.groupby(airports, key=lambda airport:airport['opendate']):
    print('Open Date:', opendate)
    for it in airport:
        print(it)

# Assign it to dictionary to reference by key later
by_opendate = {opendate: airport
               for opendate, airport in itertools.groupby(airports, key=lambda airport:airport['opendate'])}


