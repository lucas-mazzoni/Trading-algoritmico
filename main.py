from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # Para objetos de fecha y hora
import os.path  # Para administrar rutas
import sys  # Para averiguar el nombre del script (en argv[0])
import matplotlib.pyplot as plt

# Importar la plataforma backtrader
import backtrader as bt


from estrategias import estrategias

if __name__ == '__main__':
    # Crea una entidad cerebro
    cerebro = bt.Cerebro()

    #añadimos las estrategias
    cerebro.addstrategy(estrategias)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'data/KO.csv')

    # Crear un feed de datos
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2014,1,1),
        todate=datetime.datetime(2015, 12, 31),
        reverse=False)

    # Agregue la fuente de datos a Cerebro
    cerebro.adddata(data)

    # Seteamos con cuando dinero queremos arrancar
    cerebro.broker.setcash(1000000.0)

    # Un sizer determina la cantidad de activos que se comprarán o venderán en cada operación.
    cerebro.addsizer(bt.sizers.FixedSize, stake=10) 

    # Seteamos la comision de 0.1%
    cerebro.broker.setcommission(commission=0.001)

    print('Valor del portfolio inicial: %.2f' % cerebro.broker.getvalue())

    # corremos cerebro
    cerebro.run()

    # Print out the final result
    print('Valor del portfolio final: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
