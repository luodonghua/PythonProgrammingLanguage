class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, s): # cls is "Date"
        parts = s.split('-')
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    @classmethod
    def today(cls):
        import time
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

    # The goal of __repr__ is to be unambiguous
    def __repr__(self):
        return '{}-{}-{}'.format(self.year,self.month,self.day)

    # The goal of __repr__ is to be readable
    def __str__(self):
        return self.__repr__()



d = Date(2016,10,20)
e = Date.from_string('2016-10-21')
f = Date.today()

# 2016-10-20 2016-10-21 2016-10-22
print(d, e, f)