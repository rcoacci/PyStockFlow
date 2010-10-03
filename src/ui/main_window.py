# -*- coding: UTF-8 -*-
'''
Created on 29/09/2010

@author: rodrigo
'''

from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow
from core.models import Trade
from datetime import date
from main_ui import Ui_main
from ui.models import TradeModel, BrokerModel
import logging

class MainWindow(QMainWindow):

    log = logging.getLogger(__name__)

    def __init__(self, parent=None, flags=Qt.Widget):
        super(self.__class__, self).__init__(parent, flags)
        ui = Ui_main()
        self.ui = ui
        ui.setupUi(self)
        ui.trade_list.setModel(TradeModel())
        ui.broker.setModel(BrokerModel())
        ui.broker.setModelColumn(0)
        ui.date.setDate(date.today())
        ui.month.setDate(date.today())
        ui.broker.model().setRows(Broker.query.all())

    def on_month_dateChanged(self, date):
        self.load_trades()

    @QtCore.pyqtSlot()
    def on_add_clicked(self):
        ui = self.ui
        operation = ui.operation.model().operation(ui.operation.currentIndex())
        broker = ui.broker.model().getRows()[ui.broker.currentIndex()]
        trade = Trade(stock=ui.stock.text(),
                      date=ui.date.date(),
                      type=operation,
                      price=float(ui.price.text()),
                      quantity=int(ui.quantity.text()),
                      broker=broker)
        trade.calculateCost()
        trade.save()

    def load_trades(self):
        self.log.debug("Carregando trades")
        initial = date(self.ui.month.date().year(), self.ui.month.date().month(), 30)
        final = date(self.ui.month.date().year(), self.ui.month.date().month() - 1, 1)
        trades = Trade.query.filter(initial <= Trade.date <= final).order_by(Trade.date).all()
        model = self.ui.trade_list.model()
        if(model):
            model.setRows(trades)
