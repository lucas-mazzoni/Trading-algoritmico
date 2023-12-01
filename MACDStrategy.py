import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('signal', 9),
    )

    def __init__(self):
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=12,plotname='Segunda Media Móvil 1(Exponencial)')
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=26,plotname='Segunda Media Móvil 2(Exponencial)')
        self.macd = bt.indicators.MACD(self.data, period_me1=self.params.macd1, period_me2=self.params.macd2, period_signal=self.params.signal)
        self.buy_signal = bt.indicators.CrossUp(self.macd.macd, self.macd.signal)
        self.sell_signal = bt.indicators.CrossDown(self.macd.macd, self.macd.signal)
        

    def next(self):
        if self.buy_signal and self.position.size == 0:
            self.buy()
        elif self.sell_signal and self.position.size > 0 :
            self.sell()
