import backtrader as bt
from datetime import datetime

class BollingerBandsStrategy(bt.Strategy):
    params = (
        ("period", 20),
        ("devfactor", 2),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Crear el indicador de Bandas de Bollinger
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #Orden de compra/venta enviada/aceptada por/a/por el broker - Nada que hacer para devolver
            return

        #Chekear si la orden ah sido completada
        #Atencion: El broker podria rechazar la orden si no hay dinero
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price,order.executed.value,order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price,order.executed.value,order.executed.comm))

            self.bar_executed = len(self) # Saving when the order was executed

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        # Lógica de la estrategia en cada paso de tiempo
        if self.order:
            return
        # Comprar si el precio cierra por debajo de la banda inferior y no tenemos una posición
        # self.position.size === 0 evalúa si la cantidad de acciones que la estrategia tiene actualmente es igual a cero.
        if self.data.close < self.bollinger.lines.bot :
            
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.order = self.buy()
            print("TENGO ESTO PA: ",self.position.size)

        # Vender si el precio cierra por encima de la banda superior y tenemos una posición
        elif self.data.close > self.bollinger.lines.top and self.position.size > 0:
            print("VENDO ESTO PA: ",self.position.size)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            self.order = self.sell()