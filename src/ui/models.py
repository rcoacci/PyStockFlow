# -*- coding: UTF-8 -*-
'''
Created on 29/09/2010

@author: rodrigo
'''
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from core.models import Trade
import sip
# Utiliza a versão 2 da API para o QVariant e para QString. Será desnecessário apra o python3
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)



class EntityTableModel(QtCore.QAbstractTableModel):

    def __init__(self, fields, flags=Qt.ItemIsEditable):
        super(EntityTableModel, self).__init__()
        self.rows = []
        self.columns = fields
        self._flags = flags

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.DisplayRole):
        if(self._is_validIndex(index)):
            entity = self.rows[index.row()]
            return getattr(entity, self.columns[index.column()])
        else:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if(self.columnCount() >= section >= 0):
            # almost string.capwords()
            colname = ' '.join(x.capitalize() for x in self.columns[section].split("_"))
            return self.tr(colname)
        else:
            raise IndexError()

    def setData(self, index, value, role=Qt.EditRole):
        if(self._is_validIndex(index)):
            try:
                entity = self.rows[index.row()]
                setattr(entity, self.columns[index.column()], value)
                return True
            except:
                return False
        else:
            return False


    def flags(self):
        return super(EntityTableModel, self).flags() | self._flags

    def setRows(self, rows):
        self.rows = list(rows)
        self.reset()

    def getRows(self):
        return list(self.rows)

    def _is_validIndex(self, index):
        return (index.isValid() and
           index.row() < self.rowCount() and
           index.column() < self.columnCount())

def TradeModel():
    return EntityTableModel(("stock", "date", "type", "price", "quantity", "broker", "cost"))

class OperationListModel(QtCore.QAbstractListModel):

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 2;

    def data(self, index, role=Qt.DisplayRole):
        if(index == 0):
            return self.tr("Comprar")
        elif(index == 1):
            return self.tr("Vender")
        else:
            return QtCore.QVariant()

    def operation(self, index):
        if(index == 0):
            return Trade.Buy
        elif(index == 1):
            return Trade.Sell
        else:
            raise IndexError()

def BrokerModel():
    return EntityTableModel(("name", "fixed_cost", "volume_cost", "custody_cost"))
