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
                record = tuple(row)
                '''
                # alternatively, represent the record using dictionary
                record = {
                    'iata':row[0],
                    'title':row[1],
                    'city':row[2],
                    'state':row[3],
                    'country':row[4],
                    'latitude':row[5],
                    'longitude':row[6],
                    'opendate':row[7]
                '''
                airports.append(record)
    return airports

airports = read_csv('airports.csv', errors='silent')
print(airports)
print(airports[0])
print(airports[0][0])

total = 0.0
for airport in airports:
    total += airport[5] + airport[6]
print ('Total is:', total)


total = 0.0
for iata,title,city,state,country,latitude,longitude,opendate in airports:
    total += latitude + longitude
print ('Total is:', total)
