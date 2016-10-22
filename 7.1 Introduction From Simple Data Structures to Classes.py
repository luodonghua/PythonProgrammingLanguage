class Holding(object):
    def __init__(self, name, date, shares, price):
        self.name = name
        self.date = date
        self.shares = shares
        self.price = price
    def cost(self):
        return self.shares * self.price
    def sell(self, nshares):
        self.shares -= nshares


h = Holding ('AA','2016-10-22',100,32.2)
print(h.name, h.shares, h.cost())
h.sell(25)
print(h.name, h.shares, h.cost())
# Same as previous line, using "getattr(obj, attribute)" to make the code generalize
print(getattr(h,"name"), getattr(h,"shares"), h.cost())