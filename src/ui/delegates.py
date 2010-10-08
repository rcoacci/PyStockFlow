# -*- coding: UTF-8 -*-
'''
Created on 06/10/2010

@author: rodrigo
'''
from PyQt4.QtGui import QStyledItemDelegate, QDateTimeEdit
from core.models import Trade
import datetime
from ui.models import OperationListModel

class DateDelegate(QStyledItemDelegate):

    def __init__(self, parent=None, pattern="%d/%m/%Y"):
        QStyledItemDelegate.__init__(self, parent)
        self.pattern = pattern

    def displayText(self, value, locale):
        """displayText ( const QVariant & value, const QLocale & locale ) """
        value = value.strftime(self.pattern)
        return QStyledItemDelegate.displayText(self, value, locale)



    def createEditor(self, parent, option, index):
        """QWidget * QStyledItemDelegate::createEditor ( QWidget * parent, const QStyleOptionViewItem & option, const QModelIndex & index )"""
        editor = QDateTimeEdit(parent)
        editor.setCalendarPopup(True)
        editor.editingFinished().connect(self.comitAndClose())
        return editor

    def commitAndClose(self):
        self.commitData.emmit(self.sender())
        self.closeEditor.emmit(self.sender())

    def setEditorData(self, editor, index):
        """void QStyledItemDelegate::setEditorData(QWidget *editor,const QModelIndex &index)"""
        editor.setDateTime(index.data())

class OperationDelegate(QStyledItemDelegate):

    operations = OperationListModel.displayMapping

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def displayText(self, value, locale):
        """displayText ( const QVariant & value, const QLocale & locale ) """

        return QStyledItemDelegate.displayText(self, self.tr(self.operations[value]), locale)

