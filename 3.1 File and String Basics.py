f = open('airports.csv')
data = f.read()
print (data)
f.close()

f = open('airports.csv','r')
for line in f:
    print(line)
f.close()

with open('airports.csv','r') as f:
    for line in f:
        print(line[0],line[1],line[-1],line[-2],line[0-5],line[:5],line[:-5], line[3-5]+line[6:8],line.strip().replace(',','-'))
        print(line.split(',')[1])
        parts=line.split(',')
        if parts[6].strip() != 'longitude':
            print(float(parts[5]) * float(parts[6].strip()))


