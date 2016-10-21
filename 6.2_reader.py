# reader.py
import csv
def read_csv(filename, types, *, errors='warn'):
    '''
    Read the CSV with type conversion into a list of dictionary
    '''

    if errors not in {'warn', 'silent', 'raise'}:
        raise ValueError("errors must be in one of 'warn', 'silent', 'raise'")

    records = []       # list of records
    with open(filename,'r') as f:
            rows = csv.reader(f)
            headers = next(rows)           # Skill a single line input
            for rowno, row in enumerate(rows, start=1):
                try:
                    row = [ func(val) for func, val in zip(types, row)]
                except ValueError as err: # Exception is the top level exception to catch all (dangerous)
                    if errors == 'warn':
                        print('Row:', rowno, 'Bad row:', row)
                        print('Row:', rowno, 'Reason:', err)
                    elif errors == 'raise':
                        raise      # Re-raise the last exception
                    else:
                        pass
                    continue    # skip to the next line
                record = dict(zip(headers, row))
                records.append(record)
    return records