guest = ('A','B','C','D','E','F','G')
buddy = []
seated = []

i = 0

for seat1 in guest:
  seated.append(seat1)
  for seat2 in guest:
    if (seat2 in seated):
      continue
    else:
      seated.append(seat2)

      for seat3 in guest:
        if seat3 in seated: 
          continue
        else:
          seated.append(seat3)

          for seat4 in guest:
            if seat4 in seated: 
              continue
            else:
              seated.append(seat4)

              for seat5 in guest:
                if seat5 in seated: 
                  continue
                else:
                  seated.append(seat5)

                  for seat6 in guest:
                    if seat6 in seated:  
                      continue
                    else:
                      seated.append(seat6)

                      for seat7 in guest:
                        if seat7 in seated: 
                          continue
                        else:
                          seated.append(seat7)
                          if (  (seat1+seat2 not in buddy) 
                            and (seat2+seat1 not in buddy)
                            and (seat2+seat3 not in buddy)
                            and (seat3+seat2 not in buddy)
                            and (seat3+seat4 not in buddy)
                            and (seat4+seat3 not in buddy)
                            and (seat4+seat5 not in buddy)
                            and (seat5+seat4 not in buddy)
                            and (seat5+seat6 not in buddy)
                            and (seat6+seat5 not in buddy)
                            and (seat6+seat7 not in buddy)
                            and (seat7+seat6 not in buddy)
                            and (seat7+seat1 not in buddy)
                            and (seat1+seat7 not in buddy)):
                              print ("{},{},{},{},{},{},{}".format(seat1,seat2,seat3,seat4,seat5,seat6,seat7))                          
                              buddy.append(seat1+seat2)
                              buddy.append(seat2+seat1)
                              buddy.append(seat2+seat3)
                              buddy.append(seat3+seat2)
                              buddy.append(seat3+seat4)
                              buddy.append(seat4+seat3)
                              buddy.append(seat4+seat5)
                              buddy.append(seat5+seat4)
                              buddy.append(seat5+seat6)
                              buddy.append(seat6+seat5)
                              buddy.append(seat6+seat7)
                              buddy.append(seat7+seat6)
                              buddy.append(seat7+seat1)
                              buddy.append(seat1+seat7)
                              i = i + 1

                          seated.remove(seat7)
                      seated.remove(seat6)
                  seated.remove(seat5)
              seated.remove(seat4)
          seated.remove(seat3)
      seated.remove(seat2)
  seated.remove(seat1)
         

print ('Total count: {}'.format(i))      
#print (buddy)
