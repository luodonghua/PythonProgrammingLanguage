import datetime
import csv


with open('airports.csv','r') as f:
    rows = csv.reader(f)
    headers = next(rows)           # Skill a single line input
    for row in rows:
        row[5] = float(row[5])
        row[6] = float(row[6])
        row[7] = datetime.datetime.strptime(row[7], '%Y-%m-%d')
        print(row)
