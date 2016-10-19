import datetime
import csv

def csvreader_example(filename):
    '''
    :param filename:
    :return total
    Example to demonstrate functions
    '''
    total = 0.0
    with open(filename,'r') as f:
            rows = csv.reader(f)
            headers = next(rows)           # Skill a single line input
            for row in rows:
                row[5] = float(row[5])
                row[6] = float(row[6])
                row[7] = datetime.datetime.strptime(row[7], '%Y-%m-%d')
                total += row[5]
    return total

print('Total is: ', csvreader_example('airports.csv'))

import glob
files=glob.glob('airport*.csv')
for filename in files:
    print('Total is: ', csvreader_example(filename))

help(csvreader_example)