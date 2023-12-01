import backtrader as bt
from datetime import datetime
import matplotlib.pyplot as plt

class estrategias(bt.Strategy):
    params = (
        ("period", 20), # Bollinger, periodo de la media movil simple (SMA)
        ("devfactor", 2), # Bollinger,factor de desviacion estandar
        ('macd1', 12),  # MACD,periodo de la primera media movil exponencial (EMA)
        ('macd2', 26),  # MACD,periodo de la segunda media movil exponencial (EMA)
        ('signal', 9),  # MACD,periodo de la media movil exponencial (EMA) que se utiliza como linea de senial
        ("rsi_period", 14), # RSI , periodo utilizado para calcularlo.
        ("rsi_overbought", 70),# RSI, nivel que se considera sobrecompra.
        ("rsi_oversold", 30),# RSI, nivel que se considera sobreventa. 
        )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.net_profit_positive_count = 0
        self.net_profit_negative_count = 0
        # Crear el indicador de Bandas de Bollinger
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)
        # Creo indicador MACD
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=12,plotname='Segunda Media Movil 1(Exponencial)')
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=26,plotname='Segunda Media Movil 2(Exponencial)')
        self.macd = bt.indicators.MACD(self.data, period_me1=self.params.macd1, period_me2=self.params.macd2, period_signal=self.params.signal)
        self.buy_signal = bt.indicators.CrossUp(self.macd.macd, self.macd.signal)
        self.sell_signal = bt.indicators.CrossDown(self.macd.macd, self.macd.signal)
        # Creo indicador RSI
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_trade(self, trade):
        if trade.isclosed:
            if trade.pnl > 0:
                self.net_profit_positive_count += 1
            elif trade.pnl < 0:
                self.net_profit_negative_count += 1

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #Orden de compra/venta enviada/aceptada por/a/por el broker - Nada que hacer para devolver
            return

        # Chequear si la orden ah sido completada
        # Atencion: El broker podria rechazar la orden si no hay dinero
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Compra con exito, Precio: %.2f, Costo: %.2f, Comision %.2f' %(order.executed.price,order.executed.value,order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('Venta con exito, Precio: %.2f, Costo: %.2f, Comision %.2f' %(order.executed.price,order.executed.value,order.executed.comm))

            self.bar_executed = len(self) # Saving when the order was executed

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def next(self):
        if self.order:
            return
        if self.position.size == 0 :
            if (self.data.close < self.bollinger.lines.bot) or (self.buy_signal) or (not self.position and self.rsi < self.params.rsi_oversold):
                self.log('CREAR COMPRA, %.2f' % self.dataclose[0])
                self.order = self.buy()
        elif self.position.size > 0 :
            if (self.data.close > self.bollinger.lines.top and self.position.size > 0) or (self.sell_signal and self.position.size > 0) or ( not self.position and self.rsi > self.params.rsi_overbought):
                self.log('CREAR VENTA, %.2f' % self.dataclose[0])
                self.order = self.sell()
                