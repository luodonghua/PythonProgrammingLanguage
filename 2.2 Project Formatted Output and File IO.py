# Find out how long to payoff a mortgage


principal = 500000
payment = 2648.11
rate = 0.05
total_paid = 0

# Extra payment info
extra_payment = 1000
extra_payment_start_month = 1
extra_payment_end_month = 60
month = 0

out = open('d:\\temp\\schedule.txt','w') # open file for write

print('{:>5s} {:>10s} {:>10s} {:>10s}'.format('Month','Interest','Principal','Remaining'))
print('{:>5s} {:>10s} {:>10s} {:>10s}'.format('Month','Interest','Principal','Remaining'), file=out)
while principal > 0:
    month += 1
    if month >= extra_payment_start_month and month <=extra_payment_end_month:
        total_payment = payment + extra_payment
    else:
        total_payment = payment
    interest = principal *(rate/12)
    principal = principal+interest-total_payment
    total_paid += payment
    print('{:>5d} {:>10.2f} {:>10.2f} {:> 10.2f}'. format(month, interest, total_payment - interest, principal))
    print('{:>5d} {:>10.2f} {:>10.2f} {:> 10.2f}'. format(month, interest, total_payment - interest, principal), file=out)

out.close()

#2 decimal places, with , comma separator
print('Total paid:{:,.2f} in month:{}'.format(total_paid, month)) # new stype
# print('Total paid:%.2f in month:%d' % (total_paid, month)) # old style, missing comma sepator


# name = 'IBM'
# shares = 100
# price = 32.2
# print ('%10s %10d %10.2f' % (name, shares, price))
# print ('{:>10s} {:>10d} {:>10.2f}'.format(name, shares, price)) # >, <, right/left indent


OUTPUT='''
"C:\Program Files (x86)\Python35-32\python.exe" "C:/Python/PythonProgrammingLanguage/2.2 Project Formatted Output and File IO.py"
Month   Interest  Principal  Remaining
    1    2083.33    1564.78  498435.22
    2    2076.81    1571.30  496863.93
    3    2070.27    1577.84  495286.08
    4    2063.69    1584.42  493701.67
'''