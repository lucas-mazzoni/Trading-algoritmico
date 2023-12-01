import backtrader as bt

class SimpleMovingAverageStrategy(bt.Strategy):
    params = (
        ("short_period", 20),
        ("long_period", 50),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)

    def next(self):
        if self.short_ma > self.long_ma and self.position.size == 0:
            # Buy signal
            self.buy()
        elif self.short_ma < self.long_ma and self.position.size > 0:
            # Sell signal
            self.sell()
            