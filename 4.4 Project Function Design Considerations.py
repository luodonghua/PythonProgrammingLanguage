import datetime
import csv

# Never catch error if action can't be taken or meaningless to handle at that point

# any argument after * can't use positional assignment
# def csvreader_example(filename, *, errors='warn'):
# Error will ve triggered if csvreader_example('airports.csv','silent') called

def csvreader_example(filename, errors='warn'):
    '''
    :param filename:
    :return total
    Example to demonstrate functions
    '''
    if errors not in {'warn', 'silent', 'raise'}:
        raise ValueError("errors must be in one of 'warn', 'silent', 'raise'")
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
                total += row[5]
    return total

print('Total is:', csvreader_example('airports.csv', errors='silent'))
