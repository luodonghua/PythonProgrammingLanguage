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

while principal > 0:
    month += 1
    if month >= extra_payment_start_month and month <=extra_payment_end_month:
        total_payment = payment + extra_payment
    else:
        total_payment = payment
    interest = principal *(rate/12)
    principal = principal+interest-total_payment
    total_paid += payment
    print('Current principal: ', principal)

#2 decimal places, with , comma separator
print('Total paid:{:,.2f} in month:{}'.format(total_paid, month)) # new stype
print('Total paid:%.2f in month:%d' % (total_paid, month)) # old style, missing comma sepator