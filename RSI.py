import backtrader as bt

class RSI(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)


    def next(self):
        if not self.position:  # No estamos en una posición
            if self.rsi < self.params.rsi_oversold:
                # RSI por debajo del umbral de sobreventa, comprar
                self.buy()
        else:
            if self.rsi > self.params.rsi_overbought:
                # RSI por encima del umbral de sobrecompra, vender
                self.sell()