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
            rowno = 0
            for row in rows:
                rowno += 1  # alternatively use enumerate: for rowno, row in enumerate(rows, start=1)
                try:
                    row[5] = float(row[5])
                    row[6] = float(row[6])
                    row[7] = datetime.datetime.strptime(row[7], '%Y-%m-%d')
                except ValueError as err: # Exception is the top level exception to catch all
                    print('Row:', rowno, 'Bad row:', row)
                    print('Row:', rowno, 'Reason:', err)
                    continue    # skip to the next line
                total += row[5]
    return total

print('Total is:', csvreader_example('airports.csv'))
