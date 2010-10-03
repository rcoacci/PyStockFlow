# -*- coding: UTF-8 -*-
'''
Created on 28/09/2010

@author: rodrigo
'''
import logging
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger(__name__).debug("Inicializando")

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    from ui.main_window import MainWindow
    import sys
    import core
    core.models.initDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
