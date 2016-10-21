import reader

airports = reader.read_csv('airports.csv', [str,str,str,str,str,float,float,str])

for i in range(3):
    print(airports[i]['title'],airports[i]['opendate'])