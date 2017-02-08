from decimal import Decimal


class Tick(object):
    def __init__(self, symbol, price, quantity):
        assert isinstance(symbol, basestring)
        assert isinstance(price, Decimal)
        assert isinstance(quantity, int)
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
