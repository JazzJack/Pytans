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

    def setData(self, row, attr, value):
        if attr in self.model.userAttributes:
            col = self.model.userAttributes.index(attr)
            role = QtCore.Qt.UserRole
        elif attr in self.model.columnAttributes:
            col = self.model.columnAttributes.index(attr)
            role = QtCore.Qt.DisplayRole
        else :
            return
        model_index = self.model.index(row, col)
        self.model.setData(model_index, value, role)

    def getData(self, row, attr):
        if attr in self.model.userAttributes:
            col = self.model.userAttributes.index(attr)
            role = QtCore.Qt.UserRole
        elif attr in self.model.columnAttributes:
            col = self.model.columnAttributes.index(attr)
            role = QtCore.Qt.DisplayRole
        else :
            return
        model_index = self.model.index(row, col)
        return self.model.data(model_index, role)


    def on_add_action(self):
        rowCnt = self.model.rowCount()
        self.model.insertRows(rowCnt, 1)

    def on_remove_action(self):
        selectedRows = [self.proxyModel.mapToSource(index).row() for index in self.selectionModel.selectedRows()]
        for s in selectedRows:
            self.model.removeRows(s, 1)

    def on_next_action(self):
        row_of_first = self.proxyModel.mapToSource(self.proxyModel.index(0, 0)).row()
        # if first one is active : end his turn!
        if self.getData(row_of_first, "active"):
            self.setData(row_of_first, "active", False)
            self.setData(row_of_first, "acted", True)

        # if new first one hasn't acted yet : start his turn
        row_of_first = self.proxyModel.mapToSource(self.proxyModel.index(0, 0)).row()
        if not self.getData(row_of_first, "acted"):
            ap = self.getData(row_of_first, "AP")
            apGain = self.getData(row_of_first, "APGain")
            apMax = self.getData(row_of_first, "GE")
            self.setData(row_of_first, "active", True)
            self.setData(row_of_first, "AP", min(apMax, ap + apGain))
        else :
            # start new round
            for i in range(self.model.rowCount()):
                self.setData(i, "acted", False)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f1 = Fighter("Hugo", 7, 11)
    f2 = Fighter("Karl", 2, 15)
    f3 = Fighter("David Hasselhoff", 1, 7)

    model = GenericTableModel(
        data= [f1, f2, f3],
        headers= ["Name", "AP", "SN", "GE", "IN"],#, "Acted", "Active"],
        attributes= ["name", "AP", "SN", "GE", "IN", "acted", "active"],
        userAttributes= ["priority", "active", "acted", "AP", "APGain"],
        defaultNode= Fighter("", 0, 10))
    w = CombatManagerMain(model)
    w.show()

    sys.exit(app.exec_())

