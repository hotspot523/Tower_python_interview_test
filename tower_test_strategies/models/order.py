

class Order(object):
    SIDE_BUY = 1
    SIDE_SELL = 2

    def __init__(self, side, quantity, symbol):
        self.side = side
        self.quantity = quantity
        self.symbol = symbol
