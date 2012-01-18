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
        self.setupUi(self)

        self.model = model
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSortRole(QtCore.Qt.UserRole)
        self.proxyModel.sort(sortCol)
        self.combatTable.setModel(self.proxyModel)
        self.selectionModel = self.combatTable.selectionModel()

        self.actionAdd.triggered.connect(self.on_add_action)
        self.actionRemove.triggered.connect(self.on_remove_action)
        self.actionNext.triggered.connect(self.on_next_action)

    def on_add_action(self):
        rowCnt = self.model.rowCount()
        self.model.insertRows(rowCnt, 1)

    def on_remove_action(self):
        selectedRows = [self.proxyModel.mapToSource(index).row() for index in self.selectionModel.selectedRows()]
        for s in selectedRows:
            self.model.removeRows(s, 1)

    def on_next_action(self):
        # get first in list
        first_active = self.proxyModel.mapToSource(self.proxyModel.index(0, 1))
        first_acted = self.proxyModel.mapToSource(self.proxyModel.index(0, 2))

        # if first one is active : end his turn!
        if self.model.data(first_active, QtCore.Qt.UserRole):
            self.model.setData(first_active, False, role = QtCore.Qt.UserRole)
            self.model.setData(first_acted, True, role = QtCore.Qt.UserRole)

        # if new first one hasn't acted yet : start his turn
        newFirst_active = self.proxyModel.mapToSource(self.proxyModel.index(0, 1))
        newFirst_acted = self.proxyModel.mapToSource(self.proxyModel.index(0, 2))
        newFirst_AP = self.proxyModel.mapToSource(self.proxyModel.index(0, 3))
        newFirst_APGain = self.proxyModel.mapToSource(self.proxyModel.index(0, 4))
        if not self.model.data(newFirst_acted, QtCore.Qt.UserRole):
            apGain = self.model.data(newFirst_APGain, role=QtCore.Qt.UserRole)
            ap = self.model.data(newFirst_AP, role=QtCore.Qt.UserRole)
            self.model.setData(newFirst_active, True, role = QtCore.Qt.UserRole)
            self.model.setData(newFirst_AP, ap + apGain, role=QtCore.Qt.UserRole)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f1 = Fighter("Hugo", 7, 11)
    f2 = Fighter("Karl", 2, 15)
    f3 = Fighter("David Hasselhoff", 1, 7)

    model = GenericTableModel(
        data= [f1, f2, f3],
        headers= ["Name", "AP", "SN", "IN"],
        attributes= ["name", "AP", "SN", "IN", "active"],
        userAttributes= ["priority", "active", "acted", "AP", "APGain"],
        defaultNode= Fighter("", 0, 10))
    w = CombatManagerMain(model)
    w.show()

    sys.exit(app.exec_())