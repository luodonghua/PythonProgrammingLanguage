import datetime

with open('airports.csv','r') as f:
    headers = next(f)           # Skill a single line input
    for line in f:
        line = line.strip()     # Strip whitespace
        parts = line.split(',')
        parts[0] = parts[0].strip()
        parts[5] = parts[5].strip()
        parts[7] = parts[7].strip()
        parts[5] = float(parts[5])
        parts[7] = datetime.datetime.strptime(parts[7], '%Y-%m-%d')
        print(parts)
