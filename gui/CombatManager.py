#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

import sys
from PyQt4 import QtGui, QtCore, uic
from fighter import Fighter
from TableModel import GenericTableModel


base, form = uic.loadUiType("prototyp1.ui")

class CombatManagerMain(base, form):
    def __init__(self, model, parent=None, sortCol = 0):
        super(base, self).__init__(parent)

        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSortRole(QtCore.Qt.UserRole)
        self.proxyModel.sort(sortCol)


        self.setupUi(self)
        self.combatTable.setModel(self.proxyModel)
        #self.combatTable.setSortingEnabled(True)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f1 = Fighter("Hugo", 7, 11)
    f2 = Fighter("Karl", 2, 15)
    f3 = Fighter("David Hasselhoff", 1, 7)

    model = GenericTableModel(
        data= [f1, f2, f3],
        headers= ["Name", "AP", "SN", "IN"],
        attributes= ["name", "AP", "SN", "IN", "priority"],
        userAttributes= ["priority"],
        defaultNode= Fighter("", 0, 10))
    w = CombatManagerMain(model)
    w.show()

    sys.exit(app.exec_())