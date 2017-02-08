from decimal import Decimal
from tower_test_strategies.models.order import Order
from tower_test_strategies.models.tick import Tick
from tower_test_strategies.strategies.scalping_strategy import ScalpingStrategy

__author__ = 'mrossini'

from unittest import TestCase, main

class ScalpingStrategyTest(TestCase):
    LOSS_LIMIT = Decimal('.1')
    SCALP_THRESHOLD = Decimal('.15')
    AAPL = "AAPL"
    GOOG = "GOOG"


    def test_buy_after_four_rises(self):
        """
        Our strategy should place a buy order for 100 shares of a stock at market
        on the fourth increasing tick in a row.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 200)))
        order = scalp.handle_tick(tick=Tick(self.AAPL, Decimal('545.2'), 200))
        self.assertIsNotNone(order)
        self._assertCorrectBuy(order)

    def test_must_not_buy_when_position_held(self):
        """
        Our strategy should not place another 'buy' order until we have cleared our previous position.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 200)))
        self.assertIsNotNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.2'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.3'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.4'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.10'), 100)))

    def test_sell_at_loss_limit(self):
        """
        if we are down more than our loss limit we should cut our losses.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 200)))
        self.assertIsNotNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.2'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('540.1'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('530.1'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('500.1'), 100)))
        order = scalp.handle_tick(tick=Tick(self.AAPL, Decimal('488.0') , 200))
        self.assertIsNotNone(order)
        self.assertEqual(Order.SIDE_SELL, order.side)
        self.assertEqual(100, order.quantity)
        self.assertEqual(self.AAPL, order.symbol)

    def test_sell_to_take_profit(self):
        """
        Once we pass our scalping threshold we should take our profits.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 200)))
        self.assertIsNotNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.2'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('587.1'), 100)))
        order = scalp.handle_tick(tick=Tick(self.AAPL, Decimal('743.2'), 200))
        self.assertEqual(Order.SIDE_SELL, order.side)
        self.assertEqual(100, order.quantity)
        self.assertEqual(self.AAPL, order.symbol)

    def test_handle_multiple_symbols(self):
        """
        Make sure we differentiate between symbols when handling ticks.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.GOOG, Decimal('544.1'), 200)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.2'), 100)))
        order = scalp.handle_tick(tick=Tick(self.AAPL, Decimal('587.1'), 100))
        self.assertIsNotNone(order)
        self._assertCorrectBuy(order)

    def test_decrease_tick(self):
        """
        A price decrease should reset our counter.
        """
        scalp = ScalpingStrategy(self.LOSS_LIMIT, self.SCALP_THRESHOLD)
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.5'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('543.7'), 100)))
        self.assertIsNone(scalp.handle_tick(tick=Tick(self.AAPL, Decimal('544.1'), 200)))
        order = scalp.handle_tick(tick=Tick(self.AAPL, Decimal('545.2'), 200))
        self.assertIsNotNone(order)
        self._assertCorrectBuy(order)


    def _assertCorrectBuy(self, order):
        self.assertEqual(order.side, Order.SIDE_BUY)
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.symbol, self.AAPL)

if __name__ == '__main__':
    main()
