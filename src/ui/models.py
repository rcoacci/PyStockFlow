# -*- coding: UTF-8 -*-
'''
Created on 29/09/2010

@author: rodrigo
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from core.models import Broker, Trade
from datetime import date, timedelta
from elixir import session
import datetime
import sip
# Utiliza a versão 2 da API para o QVariant e para QString. Será desnecessário apra o python3
sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)




class EntityTableModel(QtCore.QAbstractTableModel):

    def __init__(self, fields, flags=Qt.ItemIsEditable, save_onchange=True):
        super(EntityTableModel, self).__init__()
        self.rows = []
        self.columns = fields
        self._flags = flags
        self._seave_onchange = save_onchange


    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.DisplayRole):
        if(not index.isValid()):
            return None

        if(self._is_validIndex(index) and (role == Qt.DisplayRole or role == Qt.EditRole)):
            entity = self.rows[index.row()]

            value = getattr(entity, self.columns[index.column()])
#            if(isinstance(value, (datetime.date, datetime.datetime))):
#                return QtCore.QDateTime(value)
#            else:
            return value

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if (role != Qt.DisplayRole):
            return None

        if(orientation == Qt.Horizontal):
            if(self.columnCount() >= section >= 0):
                # almost string.capwords()
                colname = ' '.join(x.capitalize() for x in self.columns[section].split("_"))
                return self.tr(colname)

        return None

    def setData(self, index, value, role=Qt.EditRole):
        print("SetData: %s" % value)
        if(self._is_validIndex(index) and index.isValid() and role == Qt.EditRole):
            try:
                entity = self.rows[index.row()]
                setattr(entity, self.columns[index.column()], value)
                if self._save_onchange:
                    session.commit()
                self.dataChanged().emit(index, index)
                return True
            except:
                return False
        else:
            return False


    def flags(self, index):
        if(index.isValid()):
            return super(EntityTableModel, self).flags(index) | self._flags
        else:
            return Qt.ItemIsEnabled

    def setRows(self, rows):
        self.beginResetModel()
        self.rows = list(rows)
        self.endResetModel()

    def getRows(self):
        return list(self.rows)

    def _is_validIndex(self, index):
        return (index.isValid() and
           index.row() < self.rowCount() and
           index.column() < self.columnCount())

    def load(self, *args, **kwargs):
        self.beginResetModel()
        self._loadData(*args, **kwargs)
        self.endResetModel()

    def _loadData(self, *args, **kwargs):
        raise NotImplementedError()

    def getRow(self, row):
        return self.rows[row] if 0 <= row < self.rowCount() else None

    def setRow(self, row, entity):
        if (-1 < row):
            self.rows[row] = entity
            self.dataChanged().emit(self.index(row, 0), self.index(row, self.columnCount()))

    def saveChanges(self):
        session.commit()

    def addRow(self, entity):
        session.add(entity)
        self.saveChanges()
        self.load()

    def removeRow(self, row):
        session.delete(self.getRow(row))
        self.saveChanges()
        self.load()


#class TradeModel(EntityTableModel):
#
#    def __init__(self, flags=Qt.ItemIsEditable):
#        super(TradeModel, self).__init__(("stock", "date", "type", "price", "quantity", "broker", "cost"), flags)
#
#    def _loadData(self, initial=date.today(), final=date.today() + timedelta(days=30)):
#        self.rows = Trade.query.filter(initial <= Trade.date <= final).order_by(Trade.date).all()

def TradeModel():
    return EntityTableModel(("stock", "date", "type", "price", "quantity", "broker", "cost"))

class OperationListModel(QtCore.QAbstractListModel):

    displayMapping = {Trade.Buy:"Buy", Trade.Sell:"Sell"}

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 2;

    def data(self, index, role=Qt.DisplayRole):
        if(index.row() == 0):
            return self.displayMapping[Trade.Buy]
        elif(index.row() == 1):
            return self.displayMapping[Trade.Sell]
        else:
            return None

    def operation(self, index):
        if(index == 0):
            return Trade.Buy
        elif(index == 1):
            return Trade.Sell
        else:
            raise IndexError()

#class BrokerModel(EntityTableModel):
#
#    def __init__(self, flags=Qt.ItemIsEditable):
#        super(BrokerModel, self).__init__(("name", "fixed_cost", "volume_cost", "custody_cost"), flags)
#
#    def _loadData(self):
#        self.rows = Broker.query.all()

def BrokerModel():
    return EntityTableModel(("name", "fixed_cost", "volume_cost", "custody_cost"))


