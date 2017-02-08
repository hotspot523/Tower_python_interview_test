from decimal import Decimal
from tower_test_strategies.models.order import Order
from tower_test_strategies.models.tick import Tick
from tower_test_strategies.strategies.strategy import Strategy

"""
    private final double lossLimit;
    private final double scalpThreshhold;
    private Tick priorTick;
    private int tickCount;

    public ScalpingStrategy(final double lossLimit, final double scalpThreshhold) {
        this.lossLimit = lossLimit;
        this.scalpThreshhold = scalpThreshhold;
        tickCount = 0;
    }

    @Override
    public Optional<Order> handleTick(final Tick tick) {
        tickCount++;
        if (priorTick == null) {
            priorTick = tick;
            return Optional.empty();
        }
        if (priorTick.getPrice() < tick.getPrice() && tickCount >= 4) {
            return Optional.of(new Order(Side.BUY, 100, tick.getSymbol()));
        }
        return Optional.empty();
    }
}
"""


class ScalpingStrategy(Strategy):
    total_profit = 0

    def __init__(self, loss_limit, scalp_threshold):
        assert isinstance(loss_limit, Decimal)
        assert isinstance(scalp_threshold, Decimal)
        self.loss_limit = loss_limit
        self.scalp_threshold = scalp_threshold
        self._prior_tick = None
        self._tick_count = 0

    def handle_tick(self, tick):
        assert isinstance(tick, Tick)
        self._tick_count += 1

        if not self._prior_tick:
            self._prior_tick = tick

        profit = round(((tick.price - self._prior_tick.price) / self._prior_tick.price), 2)
        self.total_profit += profit

        if self._prior_tick.price < tick.price and self._tick_count >= 4:
            self.__init__(self.loss_limit, self.scalp_threshold)
            self.total_profit = 0
            return Order(Order.SIDE_BUY, 100, tick.symbol)

        if self.total_profit < 0 and abs(self.total_profit) >= abs(self.loss_limit):
            self.__init__(self.loss_limit, self.scalp_threshold)
            self.total_profit = 0
            return Order(Order.SIDE_SELL, 100, tick.symbol)

        if self.total_profit > self.scalp_threshold:
            self.__init__(self.loss_limit, self.scalp_threshold)
            self.total_profit = 0
            return Order(Order.SIDE_SELL, 100, tick.symbol)

        if self._prior_tick.symbol != tick.symbol:
            self._tick_count -= 1
            self.total_profit -= profit
            return None

        if self._prior_tick.price > tick.price:
            self.__init__(self.loss_limit, self.scalp_threshold)
            self._tick_count += 1

        self._prior_tick = tick

        return None
